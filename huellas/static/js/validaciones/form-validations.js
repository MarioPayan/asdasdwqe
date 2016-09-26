$.getScript(base+"plugins/form-validation/dist/js/formValidation.min.js", function(){
    $.getScript(base+"plugins/form-validation/dist/js/language/es_ES.js", function() {
        $.getScript(base + "/plugins/form-validation/dist/js/framework/bootstrap.min.js", function () {
            $(document).ready(function () {
                var faIcon = {
                    valid: 'fa fa-check-circle fa-lg text-success',
                    invalid: 'fa fa-times-circle fa-lg',
                    validating: 'fa fa-refresh'
                };

                var conf_dict;
                try{
                    var this_fields = fields;
                }catch(err){
                    var this_fields = undefined;
                }
                if(this_fields){
                    conf_dict = {
                        icon: faIcon,
                        excluded: ':disabled',
                        locale: 'es_ES',
                        fields: fields
                    };
                }else {
                    conf_dict = {
                        icon: faIcon,
                        excluded: ':disabled',
                        locale: 'es_ES'
                    };
                }

                $("#rady-form").formValidation(conf_dict).on('success.field.fv', function (e, data) {
                    // $(e.target)  --> The field element
                    // data.bv      --> The BootstrapValidator instance
                    // data.field   --> The field name
                    // data.element --> The field element

                    var $parent = data.element.parents('.form-group');

                    // Remove the has-success class
                    $parent.removeClass('has-success');
                }).on('err.form.fv', function (e) {
                    isValid = false;
                });
            });
        });
    });
});