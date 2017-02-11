  $(document).ready(function() {

    var FormStuff = {

      init: function() {
        // kick it off once, in case the radio is already checked when the page loads
        this.applyConditionalRequired();
        this.bindUIActions();
      },

      bindUIActions: function() {
        // when a radio or checkbox changes value, click or otherwise
        $("input[type='radio'], input[type='checkbox']").on("change", this.applyConditionalRequired);
      },

      applyConditionalRequired: function() {
        // find each input that may be hidden or not
        $(".require-if-active").each(function() {
          var el = $(this);
          // find the pairing radio or checkbox
          if ($(el.data("require-pair")).is(":checked")) {
            // if its checked, the field should be required
            el.prop("required", true);
          } else {
            // otherwise it should not
            el.prop("required", false);
          }
        });
      }

    };

    FormStuff.init();


    $('#patient_form').bootstrapValidator({
        // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
        feedbackIcons: {
          valid: 'glyphicon glyphicon-ok',
          invalid: 'glyphicon glyphicon-remove',
          validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
          client_number: {
            validators: {
              stringLength: {
                // TODO: not sure what the minimum Client# length and Client# length are yet.
                min: 2,
              },
              notEmpty: {
                message: 'Please enter the patient&#39;s client id'
              }
            }
          },
            date_of_birth: {
              // The hidden input will not be ignored
              excluded: false,
              validators: {
                notEmpty: {
                  message: 'Please enter your date of birth.'
                },
                date: {
                  format: 'MM/DD/YYYY',
                  message: 'The date is not valid.'
                }
              }
            }
        }
      })
      .on('success.form.bv', function(e) {
        $('#success_message').slideDown({
          opacity: "show"
        }, "slow")
        $('#patient_form').data('bootstrapValidator').resetForm();

        // Prevent form submission
        e.preventDefault();

        // Get the form instance
        var $form = $(e.target);

        // Get the BootstrapValidator instance
        var bv = $form.data('bootstrapValidator');

        // Use Ajax to submit form data
        $.post($form.attr('action'), $form.serialize(), function(result) {
          console.log(result);
        }, 'json');
      });
  });
