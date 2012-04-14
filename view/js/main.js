/*
 * jQuery File Upload Plugin JS Example 6.5.1
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/*jslint nomen: true, unparam: true, regexp: true */
/*global $, window, document */

//getCookie function from w3schools.com
function getCookie(c_name)
{
var i,x,y,ARRcookies=document.cookie.split(";");
for (i=0;i<ARRcookies.length;i++)
{
  x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
  y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
  x=x.replace(/^\s+|\s+$/g,"");
  if (x==c_name)
    {
    return unescape(y);
    }
  }
}

$(function () {
    'use strict';

    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload();

    // Enable iframe cross-domain access via redirect option:
    $('#fileupload').fileupload(
        'option',
        'redirect',
        window.location.href.replace(
            /\/[^\/]*$/,
            '/cors/result.html?%s'
        )
    );

    $('#fileupload').fileupload('option', {
        url: '/upload',
        maxFileSize: 5000000,
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png|html|css|js)$/i
    });

    // Load existing files:
    $('#fileupload').each(function () {
        var that = this;
        $.getJSON(this.action, function (result) {
            if (result && result.length) {
                $(that).fileupload('option', 'done')
                    .call(that, null, {result: result});
            }
        });
    });

});
