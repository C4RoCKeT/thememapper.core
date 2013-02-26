$(function (){
    var current_hover, theme_selected, content_selected = null;
    var theme_frame = '#theme-iframe';
    var theme_selector_selected = '#theme-selector-selected';
    var theme_selector_hover = '#theme-selector-hover';
    var content_selector_selected = '#content-selector-selected';
    var content_selector_hover = '#content-selector-hover';
    var class_selected = 'theme-mapper-selected';
    var class_hover = 'theme-mapper-hover';
    $('#theme-iframe').attr('src', "/editor/iframe/theme");
    $('#theme-iframe').load(function() {
        onIframeLoad($(this));
    });
    $('#content-iframe').attr('src', "/editor/iframe/content");
    $('#content-iframe').load(function() {
        onIframeLoad($(this));
    });
    $('.theme-mapper-generate').click(function() {
        if(theme_selected == undefined && content_selected  == undefined) {
            alert('Please select a theme or content element.');
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
        }else if(rule_type == 'drop_theme') {
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

    function onIframeLoad(iframe) {
        /**
         * Add CSS to the head of the iframe.
         */
        iframe.contents().find('head').append('<style>* { cursor:crosshair !important; } .theme-mapper-hover { outline:1px solid red !important; } .theme-mapper-selected { outline:1px solid blue !important; } .theme-mapper-inline-to-inline-block { display:inline-block !important; } * { cursor:default; } </style>');
        iframe.contents().find('*').hover(
            function() {
                setHoverOutline(iframe,this);
            },
            function() {
                /**
                 * Clear the outline if you leave an element (and don't enter a new one)
                 */
                if($(this).hasClass(class_hover)) {
                    clearHoverOutline(this);
                }
            }).click(function(event) {
            event.stopPropagation();
            event.preventDefault();
            setSelected(iframe,this);
            return false;
        });
        iframe.contents().keyup(function (event) {
            var current_selected = (iframe.is(theme_frame))?theme_selected:content_selected;
            if(event.keyCode == 8 && current_selected != null) {
                event.stopPropagation();
                event.preventDefault();
                var parent = current_selected.parentNode;
                if(parent != null && parent.tagName != undefined) {
                    setSelected(iframe,parent);
                }
            }
        });
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
            $(element).addClass(class_selected);
        } else {
            clearSelected(iframe,element);
        }
    }

    function clearSelected(iframe,element) {
        if(element != null) {
            $(element).removeClass(class_selected);
            if(iframe.is(theme_frame)) {
                $(theme_selector_selected).html('');
                theme_selected = null;
            } else {
                $(content_selector_selected).html('');
                content_selected = null;
            }
        }
    }

    function clearHoverOutline(element) {
        $(element).removeClass(class_hover);
    }

    function previewRule(rule_type) {
        rule_preview = $('#rule_preview');
        rule_preview.val(generateRule(rule_type));
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
    
var myCodeMirror = CodeMirror.fromTextArea(document.getElementById("rules"), {
        mode:  "xml",
        lineNumbers: true,
        alignCDATA: true
    });
});