"use strict";

ckan.module('ekoe_data_nav', function ($) {
    return {
        initialize: function () {

            var dataIdAttribute = this.options.data_id_attribute || 'data-tab-id';
            var contentClassName = this.options.content_class_name || '.ekoe-tab-content';

            var node = this.el[0];
            var nav = node && node.querySelector('.nav');
            var tabs = nav && nav.querySelectorAll('li');
            var tabsContent = node && node.querySelectorAll(contentClassName);

            if (node) {
                node.style.display = 'block';
            }

            if (tabs && tabs.length > 0
            && tabsContent && tabsContent.length > 0) {
                // override display none css style
                nav.style.display = 'block';

                // select the first tab by default
                var selected = tabs[0].getAttribute(dataIdAttribute);
                tabs[0].setAttribute('class', 'active');

                function hideAllContents() {
                    for (var i = 0; i < tabsContent.length; i++) {
                        tabsContent[i].style.display = 'none';
                    }
                }
                function selectContent() {
                    for (var i = 0; i < tabsContent.length; i++) {
                        var id = tabsContent[i].getAttribute(dataIdAttribute);
                        if (id === selected) {
                            tabsContent[i].style.display = 'block';
                        }
                    }
                }

                hideAllContents();
                selectContent();

                for (var i = 0; i < tabs.length; i++) {
                    tabs[i].addEventListener('click', function() {
                        var tab = this;
                        selected = tab.getAttribute(dataIdAttribute);
                        // remove all classes from li tabs
                        for (var j = 0; j < tabs.length; j++) {
                            tabs[j].setAttribute('class', '');
                        }
                        // hide all contents
                        hideAllContents();
                        // set active class to the current one
                        tab.setAttribute('class', 'active');
                        selectContent();
                    });
                }
            }
        }
    };
});
