// odoo.define('act.cabacera', function (require) {
//     "use strict";
//
//     console.log('Hola se sipone que lees ')
//     $(document).ready(function () {
//         console.log("ya esta el docuemto cargado")
//         mensaje("Si se carga")
//     });
// });

function mensaje(txt) {
    Toastify({
        text: txt,
        duration: 5000,
        close: true,
        node: 'Hola',
        className: "info",
        backgroundColor: "radial-gradient(circle, rgba(216,174,238,1) 14%, rgba(64,44,131,1) 100%);",
    }).showToast();
}


function mensaje_error(txt) {
    Toastify({
        text: txt,
        duration: 5000,
        gravity: "top",
        position: 'right',
        close: true,
        node: 'Hola',
        backgroundColor: "rgb(227,21,21)",
    }).showToast();
}

// Para Validaciones del vehiculo
function eventosValidacion() {
    //Marca
    $('[name="marca"]').keyup(function () {
        $('[name="marca"]').removeClass('o_field_invalid');
        txt = $("[name='marca']").val()
        if (txt.length < 2) {
            $("[name='marca']").addClass('o_field_invalid');
        }
        $("[name='marca']").val(txt.toUpperCase());
    });
    //Modelo
    $('[name="modelo"]').keyup(function () {
        $('[name="modelo"]').removeClass('o_field_invalid');
        txt = $("[name='modelo']").val()
        if (txt.length < 2) {
            $("[name='modelo']").addClass('o_field_invalid');
        }
        $("[name='modelo']").val(txt.toUpperCase());
    });

    //SERIE
    $('[name="serie"]').keyup(function () {
        $('[name="serie"]').removeClass('o_field_invalid');
        txt = $("[name='serie']").val()
        if (txt.length < 4) {
            $("[name='serie']").addClass('o_field_invalid');
        }
        $("[name='serie']").val(txt.toUpperCase());
    });

    //NUMERO_DE_MOTOR
    $('[name="n_motor"]').keyup(function () {
        $('[name="n_motor"]').removeClass('o_field_invalid');
        txt = $("[name='n_motor']").val()
        if (txt.length < 4) {
            $("[name='n_motor']").addClass('o_field_invalid');
        }
        $("[name='n_motor']").val(txt.toUpperCase());
    });

    //NUMERO_DE_MOTOR
    $('[name="n_chasis"]').keyup(function () {
        $('[name="n_chasis"]').removeClass('o_field_invalid');
        txt = $("[name='n_chasis']").val()
        if (txt.length < 4) {
            $("[name='n_chasis']").addClass('o_field_invalid');
        }
        $("[name='n_chasis']").val(txt.toUpperCase());
    });


    //color_primario, color_secundario
    $('[name="color_primerio"], [name="color_secundario"]').keyup(function () {
        $('[name="color_primerio"]').removeClass('o_field_invalid');
        txt = $("[name='color_primerio']").val()
        if (txt.length < 4) {
            $("[name='color_primerio']").addClass('o_field_invalid');
        }
        $("[name='color_primerio']").val(txt.toUpperCase());

        $('[name="color_secundario"]').removeClass('o_field_invalid');
        txt = $("[name='color_secundario']").val()
        if (txt.length < 4) {
            $("[name='color_secundario']").addClass('o_field_invalid');
        }
        $("[name='color_secundario']").val(txt.toUpperCase());
    });

    //Coloress
    $('[name="color_primerio"], [name="color_secundario"]').bind('keydown', function (event) {
        if (event.keyCode >= 48 && event.keyCode <= 57 || event.keyCode >= 96 && event.keyCode <= 105) {
            return false
        }
    });


    //Validacion de la placa
    $('[name="placa"]').bind('keyup', function (event) {
        txt = $('[name="placa"]').val();
        $("[name='placa']").val(txt.toUpperCase());
        if (event.keyCode != 8 && event.keyCode != 46) {
            if (txt.length == 3) {
                txt = txt + "-";
                $("[name='placa']").val(txt.toUpperCase());
                return false
            }
        }
    });

    //Placa
    $('[name="placa"]').bind('keydown', function (event) {
        $("[name='placa']").removeClass('o_field_invalid');
        txt = $('[name="placa"]').val();
        $("[name='placa']").val(txt.toUpperCase());
        if (event.keyCode >= 48 && event.keyCode <= 57) {
            if (txt.length > 3) {
                if (txt.length <= 7) {
                    if (txt.length == 7)
                        mensaje("No Ingresar mas caracteres")
                } else {
                    mensaje("No se permite el ingreso de mas carateres")
                    return false
                }
            } else {
                mensaje("Necesita Ingresar letras")
                $("[name='placa']").addClass('o_field_invalid');
                return false;
            }
        }
        if (event.keyCode >= 96 && event.keyCode <= 105) {
            if (txt.length > 3) {
                if (txt.length <= 7) {
                    if (txt.length == 7)
                        mensaje("No Ingresar mas caracteres")
                } else {
                    mensaje("No se permite el ingreso de mas carateres")
                    return false
                }
            } else {
                mensaje("Necesita Ingresar letras")
                $("[name='placa']").addClass('o_field_invalid');
                return false;
            }
        }
        if (event.keyCode >= 65 && event.keyCode <= 90) {
            if (txt.length <= 3) {
                if (txt.length == 3) {
                    return false
                }
            } else if (txt.length <= 7) {
                mensaje("Necesita Ingresar Números")
                $("[name='placa']").addClass('o_field_invalid');
                return false;
            } else {
                mensaje("No se permite el ingreso de mas carateres")
                return false;
            }
        }
    });

    $(".modal-dialog .modal-content .modal-footer .btn-primary").on("click", function (event) {
            var bandera = false
            var msg = "Correquir los Siquietes Campos <br>"
            if ($("[name='marca']").val().trim().length < 2) {
                msg += "* La MARCA debe contener mas caracteres <br> "
                bandera = true
            }
            if ($("[name='modelo']").val().trim().length < 2) {
                msg += "* El MODELO debe contener mas caracteres <br> "
                bandera = true
            }
            if ($("[name='serie']").val().trim().length < 4) {
                msg += "* La SERIE debe contener mas caracteres <br> "
                bandera = true
            }
            if ($("[name='n_motor']").val().trim().length < 4) {
                msg += "* El NUMERO MOTOR debe contener mas caracteres <br> "
                bandera = true
            }
            if ($("[name='n_chasis']").val().trim().length < 4) {
                msg += "* El NUMERO CHASIS debe contener mas caracteres <br> "
                bandera = true
            }
            if ($("[name='placa']").val().trim().length < 7) {
                msg += "* Placa Incorrecta <br> "
                bandera = true
            }
            if ($("[name='color_primerio']").val().trim().length < 4) {
                msg += "* El COLOR PRIMARIO debe contener mas caracteres <br> "
                bandera = true
            }
            if (bandera) {
                msg += " <br> > Tener cuidado con los espacion en Blanco "
                mensaje_error(msg)
            }

        }
    )

}

function validar_eventos_muebles() {
    //Marca //Modelo //Serie //Color
    $('[name="marca"],[name="modelo"],[name="serie"],[name="color"]').keyup(function () {
        $('[name="marca"]').removeClass('o_field_invalid');
        $('[name="modelo"]').removeClass('o_field_invalid');
        $('[name="serie"]').removeClass('o_field_invalid');
        $('[name="color"]').removeClass('o_field_invalid');

        txt = $("[name='marca']").val()
        if (txt.length < 2) {
            $("[name='marca']").addClass('o_field_invalid');
        }
        $("[name='marca']").val(txt.toUpperCase());

        txt = $("[name='modelo']").val()
        if (txt.length < 2) {
            $("[name='modelo']").addClass('o_field_invalid');
        }
        $("[name='modelo']").val(txt.toUpperCase());

        txt = $("[name='serie']").val()
        if (txt.length < 4) {
            $("[name='serie']").addClass('o_field_invalid');
        }
        $("[name='serie']").val(txt.toUpperCase());

        txt = $("[name='color']").val()
        if (txt.length < 4) {
            $("[name='color']").addClass('o_field_invalid');
        }
        $("[name='color']").val(txt.toUpperCase());
    });

    $('[name="color"]').bind('keydown', function (event) {
        if (event.keyCode >= 48 && event.keyCode <= 57 || event.keyCode >= 96 && event.keyCode <= 105) {
            return false
        }
    });

    $('[name="largo"],[name="ancho"]').bind('keydown', function (event) {
        if (event.keyCode != 8 && event.keyCode != 46 && event.keyCode != 110 && event.keyCode != 190 && event.keyCode != 188) {
            if (event.keyCode >= 48 && event.keyCode <= 57 || event.keyCode >= 96 && event.keyCode <= 105) {
                return true
            } else {
                return false
            }
        }

    });

    $(".modal-dialog .modal-content .modal-footer .btn-primary").on("click", function (event) {
            var bandera = false
            var msg = "Correquir los Siquietes Campos <br>"

            if ($("[name='marca']").val().trim().length < 2) {
                msg += "   * La MARCA debe contener mas caracteres <br>"
                bandera = true;
            }
            if ($("[name='modelo']").val().trim().length < 2) {
                msg += "   * El MODELO debe contener mas caracteres <br>"
                bandera = true
            }
            if ($("[name='serie']").val().trim().length < 4) {
                msg += "   * La SERIE debe contener mas caracteres <br>"
                bandera = true
            }
            if ($("[name='color']").val().trim().length < 4) {
                msg += "   * El COLOR debe contener mas caracteres <br> "
                bandera = true
            }
            if (bandera) {
                msg += " <br> > Tener cuidado con los espacion en Blanco "
                mensaje_error(msg)
            }
        }
    );
}

function validar_direccions() {
    $('[name="sector"],[name="calle_principal"],[name="calle_secundaria"]').keyup(function () {
        $('[name="sector"]').removeClass('o_field_invalid');
        $('[name="calle_principal"]').removeClass('o_field_invalid');
        $('[name="calle_secundaria"]').removeClass('o_field_invalid');

        txt = $("[name='sector']").val()
        if (txt.length < 4) {
            $("[name='sector']").addClass('o_field_invalid');
        }
        $("[name='sector']").val(txt.toUpperCase());

        txt = $("[name='calle_principal']").val()
        if (txt.length < 4) {
            $("[name='calle_principal']").addClass('o_field_invalid');
        }
        $("[name='calle_principal']").val(txt.toUpperCase());

        txt = $("[name='calle_secundaria']").val()
        if (txt.length < 4) {
            $("[name='calle_secundaria']").addClass('o_field_invalid');
        }
        $("[name='calle_secundaria']").val(txt.toUpperCase());

    });

    $('[name="num_calle"]').bind('keydown', function (event) {
        if (event.keyCode != 8 && event.keyCode != 46 && event.keyCode != 189 && event.keyCode != 109) {
            if (event.keyCode >= 48 && event.keyCode <= 57 || event.keyCode >= 96 && event.keyCode <= 105) {
                return true
            } else {
                return false
            }
        }
    });

}


function validar_inmueble() {
    //Marca //Modelo //Serie //Color
    $('[name="marca"],[name="modelo"],[name="serie"],[name="pro_reg_municipio"],[name="clave_catastral"],[name="num_predio"]').keyup(function () {
        $('[name="marca"]').removeClass('o_field_invalid');
        $('[name="modelo"]').removeClass('o_field_invalid');
        $('[name="serie"]').removeClass('o_field_invalid');
        $('[name="pro_reg_municipio"]').removeClass('o_field_invalid');
        $('[name="clave_catastral"]').removeClass('o_field_invalid');
        $('[name="num_predio"]').removeClass('o_field_invalid');

        txt = $("[name='marca']").val()
        if (txt.length < 2) {
            $("[name='marca']").addClass('o_field_invalid');
        }
        $("[name='marca']").val(txt.toUpperCase());

        txt = $("[name='modelo']").val()
        if (txt.length < 2) {
            $("[name='modelo']").addClass('o_field_invalid');
        }
        $("[name='modelo']").val(txt.toUpperCase());

        txt = $("[name='serie']").val()
        if (txt.length < 4) {
            $("[name='serie']").addClass('o_field_invalid');
        }
        $("[name='serie']").val(txt.toUpperCase());

        txt = $("[name='pro_reg_municipio']").val()
        if (txt.length < 4) {
            $("[name='pro_reg_municipio']").addClass('o_field_invalid');
        }
        $("[name='pro_reg_municipio']").val(txt.toUpperCase());

        txt = $("[name='clave_catastral']").val()
        if (txt.length < 4) {
            $("[name='clave_catastral']").addClass('o_field_invalid');
        }
        $("[name='clave_catastral']").val(txt.toUpperCase());

        txt = $("[name='num_predio']").val()
        if (txt.length < 4) {
            $("[name='num_predio']").addClass('o_field_invalid');
        }
        $("[name='num_predio']").val(txt.toUpperCase());
    });
}

