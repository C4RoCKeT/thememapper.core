$(function (){
    var current_hover, theme_selected, content_selected = null;
    var theme_frame = '#theme-iframe';
    var content_frame = '#content-iframe';
    var theme_selector_selected = '#theme-selector-selected';
    var theme_selector_hover = '#theme-selector-hover';
    var content_selector_selected = '#content-selector-selected';
    var content_selector_hover = '#content-selector-hover';
    var class_selected = 'theme-mapper-selected';
    var class_hover = 'theme-mapper-hover';
    var highLighter = true;
    var childWindow = null;
    $('#loading').waiting({ 
        className: 'waiting-circles', 
        elements: 8, 
        radius: 20, 
        auto: true 
    });
    var loading = $('#loading');
    var myCodeMirror = CodeMirror.fromTextArea(document.getElementById("rules"), {
        mode:  "xml",
        lineNumbers: true,
        alignCDATA: true
    });
    loading.css('marginTop',(loading.parent().height()-loading.height())/2);
    loading.parent().hide();

    load_theme_iframe($('#template-select').val());
    $('#theme-iframe').load(function() {
        onIframeLoad($(this));
    });
    load_content_iframe();
    $('#content-iframe').load(function() {
        onIframeLoad($(this));
    });
    $('#file-tree a').click(function() {
        var path = $(this).attr('data-path').replace(theme_path,'');
        $('#theme-iframe').attr('src', "/iframe/theme"+path);
        return false;
    });
    $('#template-select').change(function() {
        load_theme_iframe($(this).val())
    });
    $('.iframe-menu a.fullscreen').click(function() {
        if($(this).attr('data-iframe') == 'theme') {
            $(theme_frame).parent().css('width','100%');
            $(theme_frame).css('height',($(window).height()-130) + 'px');
            $('#code-wrap').hide();
            $(content_frame).parent().hide();
            $('#theme-iframe-wrap .iframe-menu a.fullscreen').hide();
            $('#theme-iframe-wrap .iframe-menu a.windowed').show();
        } else  {
            $(content_frame).parent().css('width','100%');
            $(content_frame).css('height',($(window).height()-130) + 'px');
            $('#code-wrap').hide();
            $(theme_frame).parent().hide();
            $('#content-iframe-wrap .iframe-menu a.fullscreen').hide();
            $('#content-iframe-wrap .iframe-menu a.windowed').show();
        }
        return false;
    });
    $('.iframe-menu a.windowed').click(function() {
        if($(this).attr('data-iframe') == 'theme') {
            $(theme_frame).parent().css('width','');
            $(theme_frame).css('height','');
            $('#code-wrap').show();
            $(content_frame).parent().show();
            $('#theme-iframe-wrap .iframe-menu a.fullscreen').show();
            $('#theme-iframe-wrap .iframe-menu a.windowed').hide();
        } else {
            $(content_frame).parent().css('width','');
            $(content_frame).css('height','');
            $('#code-wrap').show();
            $(theme_frame).parent().show();
            $('#content-iframe-wrap .iframe-menu a.fullscreen').show();
            $('#content-iframe-wrap .iframe-menu a.windowed').hide();
        }
        return false;
    });
    $('.iframe-menu a.parent').click(function() {
        if($(this).attr('disabled') == undefined) {
            if($(this).attr('data-iframe') == 'theme') {
                select_parent_element($(theme_frame),theme_selected);
            } else {
                select_parent_element($(content_frame),content_selected);
            }
        }
        return false;
    });
    $('.iframe-menu a#highlighter').click(function() {
        highLighter = !highLighter;
        clearSelected($(content_frame),content_selected);
    });

    $('#generate-rule').click(function() {
        if($(this).attr('disabled') !== undefined || (theme_selected == undefined && content_selected  == undefined)) {
            return false;
        } else
            $('div.selector_both,div.selector_content,div.selector_theme,#theme-applyto,#content-applyto').show();
        if(theme_selected == undefined) {
            $('div.selector_theme,div.selector_both,#theme-applyto').hide();
        }
        if(content_selected == undefined) {
            $('div.selector_content,div.selector_both,#content-applyto').hide();
        }
        $('input:radio[name=rule_type]:visible:first').attr('checked',true);
        $('#rule_generate_box,.mask').show();
        $('#mask_content').css('marginTop',($('#mask').height() - $('#mask_content').height())/2 + 'px');
        previewRule();
    });
    $('#mask').click(function() {
        hideMask();
    });
    $('#mask_content,#mask_content.mask_content_block').click(function(e) {
        e.stopPropagation();
    });
    $('#rule_generate_form input:radio').change(function() {
        var rule_type = $('input:radio[name=rule_type]:checked').val();
        if(rule_type == 'drop_content') {
            $('#theme-applyto').hide();
            $('#content-applyto').show();
        }
        else if(rule_type == 'drop_theme') {
            $('#theme-applyto').show();
            $('#content-applyto').hide();
        } else {
            $('#content-applyto,#theme-applyto').show();
        }
        previewRule(rule_type);
    });
    $('#rule_generate_form input:checkbox').change(function() {
        var rule_type = $('input:radio[name=rule_type]:checked').val();
        previewRule(rule_type);
    });
    $('#rule_generate_form .button_ok').click(function() {
        var rule_type = $('input:radio[name=rule_type]:checked').val();
        var rules = $('#rules');
        myCodeMirror.setValue(myCodeMirror.getValue().replace('</rules>',"    " + generateRule(rule_type) + "\n</rules>"));
        hideMask();
    });
    $('#rule_generate_form .button_cancel').click(function() {
        hideMask();
    });
    
    function load_theme_iframe(path) {
        $('#theme-iframe').attr('src', "/iframe/theme"+path);
        return false;
    }
    
    function load_content_iframe(url) {
        if(url != undefined) {
            url = "/" + url;
        }
        else {
            url = ""
        }
        $('#view-result').attr('data-url', "/editor/result"+url);
        $('#content-iframe').attr('src', "/iframe/content"+url);
        changeChildWindowLocation("/editor/result"+url);
        return false;
    }

    function onIframeLoad(iframe) {
        /**
         * Add CSS to the head of the iframe.
         */
        iframe.contents().find('head').append('<style>* { cursor:crosshair !important; } .theme-mapper-hover { outline:1px solid red !important; } .theme-mapper-selected { outline:1px solid blue !important; } .theme-mapper-inline-to-inline-block { display:inline-block !important; } * { cursor:default; } </style>');
        iframe.contents().find('*').hover(
            function() {
                if(highLighter || iframe.is(theme_frame)) {
                    setHoverOutline(iframe,this);
                }
            },
            function() {
                /**
                 * Clear the outline if you leave an element (and don't enter a new one)
                 */
                if($(this).hasClass(class_hover)) {
                    clearHoverOutline(this);
                }
            }).click(
            function(event) {
                event.preventDefault();
                if(highLighter || iframe.is(theme_frame)) {
                    event.stopPropagation();
                    setSelected(iframe,this);
                } else if($(this).is('a')) {
                    load_content_iframe($(this).prop('href'));
                    return false;
                }
            });
        iframe.contents().find('form').submit(function(event) {
            event.preventDefault();
            return false;
        });
        iframe.contents().keyup(function (event) {
            var current_selected = (iframe.is(theme_frame))?theme_selected:content_selected;
            if(event.keyCode == 27 && current_selected != null) {
                event.stopPropagation();
                event.preventDefault();
                select_parent_element(iframe,current_selected);
            }
        });
    }

    function select_parent_element(iframe,element) {
        var parent = element.parentNode;
        if(parent != null && parent.tagName != undefined) {
            setSelected(iframe,parent);
            var grandparent = parent.parentNode;
            if(grandparent == null || grandparent.tagName == undefined) {
                disable_parent_button(iframe);
            }
        } else {
            disable_parent_button(iframe);
        }
    }

    function enable_parent_button(iframe) {
        if(iframe.is(theme_frame)) {
            $('#theme-iframe-wrap div.iframe-menu a.parent').removeAttr('disabled');
        } else {
            $('#content-iframe-wrap div.iframe-menu a.parent').removeAttr('disabled');
        }
    }

    function enable_rule_button() {
        $('#generate-rule').removeAttr('disabled');
    }

    function disable_parent_button(iframe) {
        if(iframe.is(theme_frame)) {
            $('#theme-iframe-wrap div.iframe-menu a.parent').attr('disabled','disabled');
        } else {
            $('#content-iframe-wrap div.iframe-menu a.parent').attr('disabled','disabled');
        }
    }

    function disable_rule_button() {
        $('#generate-rule').attr('disabled','disabled');
    }

    /**
     * Source: plone.app.theming mapper.js
     * Return a valid, unique XPath selector for the given element.
     */
    function calculateUniqueXPathExpression(element) {
        var parents = $(element).parents();

        function elementIndex(e) {
            var siblings = $(e).siblings(e.tagName.toLowerCase());
            if(siblings.length > 0) {
                return "[" + ($(e).index() + 1) + "]";
            } else {
                return "";
            }
        }
        var xpathString = "/" + element.tagName.toLowerCase();
        if(element.id) {
            return "/" + xpathString + "[@id='" + element.id + "']";
        } else {
            xpathString += elementIndex(element);
        }

        for(var i = 0; i < parents.length; ++i) {
            var p = parents[i];

            var pString = "/" + p.tagName.toLowerCase();

            if(p.id) {
                return "/" + pString + "[@id='" + p.id + "']" + xpathString;
            } else {
                xpathString = pString + elementIndex(p) + xpathString;
            }
        }
        return xpathString;
    }

    /**
     * Source: plone.app.theming mapper.js
     * Return a valid, unqiue CSS selector for the given element. Returns null if
     * no reasoanble unique selector can be built.
     */
    function calculateUniqueCSSSelector(element) {
        var paths = [];
        var path = null;
        var parents = $(element).parents();
        var ultimateParent = parents[parents.length - 1];
        while (element && element.nodeType == 1) {
            var selector = calculateCSSSelector(element);
            paths.splice(0, 0, selector);
            path = paths.join(" ");
            // The ultimateParent constraint is necessary since
            // this may be inside an iframe
            if($(path, ultimateParent).length == 1) {
                return path;
            }

            element = element.parentNode;
        }
        return null;
    }

    /**
     * Source: plone.app.theming mapper.js
     * Return a valid (but not necessarily unique) CSS selector for the given
     * element.
     */
    function calculateCSSSelector(element) {
        var selector = element.tagName.toLowerCase();
        if (element.id) {
            selector += "#" + element.id;
        } else {
            var classes = $(element).attr('class');
            if(classes != undefined) {
                var splitClasses = classes.split(/\s+/);
                for(var i = 0; i < splitClasses.length; ++i) {
                    if(splitClasses[i] != "" && !splitClasses[i].indexOf('theme-mapper') == 0) {
                        selector += "." + splitClasses[i];
                        break;
                    }
                }
            }
        }
        return selector;
    }

    function bestSelector(element) {
        return calculateUniqueCSSSelector(element) || calculateUniqueXPathExpression(element);
    }

    function isSelected(element) {
        return $(element).hasClass(class_selected);
    }

    function setHoverOutline(iframe,element) {
        var selector_view = (iframe.is(theme_frame))?theme_selector_hover:content_selector_hover;
        if(current_hover != null) {
            clearHoverOutline(current_hover);
        }
        current_hover = element;
        $(element).addClass(class_hover);
        $(selector_view).html(bestSelector(element));
    }

    function setSelected(iframe,element) {
        if(!isSelected(element)) {
            var selector = bestSelector(element);
            if(iframe.is(theme_frame)) {
                clearSelected(iframe,theme_selected);
                $(theme_selector_selected).html(selector);
                theme_selected = element;
            } else {
                clearSelected(iframe,content_selected);
                $(content_selector_selected).html(selector);
                content_selected = element;
            }
            enable_parent_button(iframe);
            enable_rule_button();
            $(element).addClass(class_selected);
        } else {
            clearSelected(iframe,element);
        }
    }

    function clearSelected(iframe,element) {
        if(element != null) {
            $(element).removeClass(class_selected);
            if(iframe.is(theme_frame)) {
                $('#theme-iframe-wrap div.iframe-menu a.parent').attr('disabled','disabled');
                $(theme_selector_selected).html('');
                theme_selected = null;
            } else {
                $('#content-iframe-wrap div.iframe-menu a.parent').attr('disabled','disabled');
                $(content_selector_selected).html('');
                content_selected = null;
            }
            if(theme_selected == undefined && content_selected  == undefined) {
                disable_rule_button();
            }
        }
    }

    function clearHoverOutline(element) {
        $(element).removeClass(class_hover);
    }

    function previewRule(rule_type) {
        $('#rule_preview').val(generateRule(rule_type));
    }

    function hideMask() {
        $('#mask_content.mask_content_block,.mask').hide();
    }

    function generateRule(rule_type) {
        var rule = '';
        switch(rule_type) {
            default:
            case 'replace':
                if(content_selected != undefined && theme_selected != undefined) {
                    rule = '<replace ' +
                    calculateDiazoSelector(content_selected,'content',$('input:checkbox[name=checkbox_content_children]').is(':checked')) + ' ' +
                    calculateDiazoSelector(theme_selected,'theme',$('input:checkbox[name=checkbox_theme_children]').is(':checked')) + ' />';
                }
                break;
            case 'before':
                if(content_selected != undefined && theme_selected != undefined) {
                    rule = '<before ' +
                    calculateDiazoSelector(content_selected,'content',$('input:checkbox[name=checkbox_content_children]').is(':checked')) + ' ' +
                    calculateDiazoSelector(theme_selected,'theme',$('input:checkbox[name=checkbox_theme_children]').is(':checked')) + ' />';
                }
                break;
            case 'after':
                if(content_selected != undefined && theme_selected != undefined) {
                    rule = '<after ' +
                    calculateDiazoSelector(content_selected,'content',$('input:checkbox[name=checkbox_content_children]').is(':checked')) + ' ' +
                    calculateDiazoSelector(theme_selected,'theme',$('input:checkbox[name=checkbox_theme_children]').is(':checked')) + ' />';
                }
                break;
            case 'drop_content':
                if(content_selected != undefined) {
                    rule = '<drop ' + calculateDiazoSelector(content_selected,'content',$('input:checkbox[name=checkbox_content_children]').is(':checked')) +' />';
                }
                break;
            case 'drop_theme':
                if(theme_selected != undefined) {
                    rule = '<drop ' + calculateDiazoSelector(theme_selected,'theme',$('input:checkbox[name=checkbox_theme_children]').is(':checked')) +' />';
                }
                break;

        }
        return rule;
    }

    /**
     * Source: plone.app.theming mapper.js
     * Build a Diazo selector element with the appropriate namespace.
     */
    function calculateDiazoSelector(element, scope, children) {
        var selectorType = scope;
        if(children) {
            selectorType += "-children";
        }

        var cssSelector = calculateUniqueCSSSelector(element);
        if(cssSelector) {
            return "css:" + selectorType + "=\"" + cssSelector + "\"";
        } else {
            var xpathSelector = calculateUniqueXPathExpression(element);
            return selectorType + "=\"" + xpathSelector + "\"";
        }

    }

    $('#view-result').click(function (event) {
        event.preventDefault();
        openChildWindow($(this).attr('data-url'));
        return false;
    });

    function openChildWindow(url) {
        childWindow = window.open(url);
    }
      
    function refreshChildWindow() {
        if (childWindow)
            childWindow.location.reload();
    }

    function unloadChildWindow() {
        childWindow = null;
    }

    function changeChildWindowLocation(url) {
        if (childWindow) {
            childWindow.location = 'http://' + childWindow.location.host + url;
        }
    }
    
    function loadRules(path) {
        $('#rules-select').attr('disabled','disabled');
        $('#rules-reload,#rules-save').addClass('disabled');
        loading.parent().fadeIn(100);
        $.post('/ajax/rules/load',{
            path:path
        },function(data) {
            myCodeMirror.setValue(data);
            loading.css('marginTop',(loading.parent().height()-loading.height())/2);
            loading.parent().fadeOut(250);
            $('#rules-select').removeAttr('disabled');
            $('#rules-reload,#rules-save').removeClass('disabled');
        },'text');
    }
    
    function saveRules(data) {
        $('#rules-reload').addClass('disabled');
        $('#rules-save').button('loading').addClass('disabled');
        $('#rules-select').attr('disabled','disabled');
        loading.parent().fadeIn(100);
        $.post('/ajax/rules/save',data,function(){
            if(childWindow != undefined) {
                refreshChildWindow();
            }
            loading.parent().fadeOut(250);
            $('#rules-save').button('reset').removeClass('disabled');
            $('#rules-reload').removeClass('disabled');
            $('#rules-select').removeAttr('disabled');
        });
    }
    
    $('#rules-reload').click(function(){
        if(!$(this).hasClass('disabled')) {
            loadRules($('#rules-select').val());
        }
    });
    
    $('#rules-select').change(function(){
        loadRules($('#rules-select').val());
    });
    
    $('#rules-save').click(function() {
        if(!$(this).hasClass('disabled')) {
            myCodeMirror.save();
            saveRules($('#rules-form').serialize());
        }
    });
    
});