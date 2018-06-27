//通用ajax表单提交
function ajaxForm(formObj, redrectUrl) {
    formObj.submit(function () {
        $.ajax({
            url: formObj.attr('action'),
            data: formObj.serialize(),
            method: 'post',
            success: function (retData) {
                if (retData.errcode == 0) {
                    alert(retData.msg)
                    setTimeout(function () {
                        window.location.href = redrectUrl;
                    }, 1000);
                } else {
                    alert(retData.msg)
                }
            },
            error: function () {
                alert('Sorry!There are something wrong in server!');
            }
        });
        return false;
    });

}


//带编辑器的表单提交


function ajaxFormWithEditor(formObj, redrectUrl, editId) {
    formObj.submit(function () {
        var textValue = document.getElementById(editId);
        textValue.value = tinyMCE.getInstanceById(editId).getBody().innerHTML;
        $.ajax({
            url: formObj.attr('action'),
            data: formObj.serialize(),
            method: 'post',
            success: function (retData) {
                if (retData.errcode == 0) {
                    alert(retData.msg)
                    setTimeout(function () {
                        window.location.href = redrectUrl;
                    }, 1000);
                } else {
                    alert(retData.msg)
                }
            },
            error: function () {
                alert('Sorry!There are something wrong in server!');
            }
        });
        return false;
    });

}