const $email_validation = document.getElementById('email_validation');
const $contrasena_validation = document.getElementById('contrasena_validation');
const $formularioempleado = document.getElementById('formularioempleado');
var $expresion_email, $expresion_password;


$expresion_email = /^([\da-z_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/;
$expresion_password = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;


(function() {
    $formularioempleado.addEventListener('submit', function(e) {
        let email=String($email_validation.value).trim();
        let contrasena=String($contrasena_validation.value).trim();

        if(email.length === 0 || contrasena.length === 0){
            alert("Todos los campos son obligatorios");
            e.preventDefault();
        }
        else if(email.length>100){
            alert("El correo es muy largo");
            e.preventDefault();
        }
        else if(!$expresion_email.test(email)){
            alert("El correo no es valido");
            e.preventDefault();
        }
        else if(contrasena.length>255){
            alert("La Contraseña es muy larga");
            e.preventDefault();
        }
        else if(!$expresion_password.test(contrasena)){
            alert("Contraseña: Debe contener al menos un numero y una letra mayúscula y minúscula, y al menos 8 caracteres o más");
            e.preventDefault();
        }

        e.preventDefault();
    });

})();

/*function validarlogin(){
    var rut_validator, email_validator, contrasena_validator, expresion_email, expresion2_password, expresion_nombres, expresion_apellidos;

    email_validator = document.getElementById("email_validation").value;
    contrasena_validator = document.getElementById("contrasena_validation").value;

    

    expresion_email = /^([\da-z_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/;
    expresion2_password = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
    expresion_nombres = /^([^0-9]*)$/;
    expresion_apellidos = /^([^0-9]*)$/;
    expresion_rut = /^[0-9]*$/
    



    if(email_validator === "" || contrasena_validator === ""){
        alert("Todos los campos son obligatorios");
        return false;

    }
    else if(email_validator.length>100){
        alert("El correo es muy largo");
        return false;
    }
    else if(!expresion_email.test(email_validator)){
        alert("El correo no es valido");
        return false;
    }
    else if(contrasena_validator.length>255){
        alert("La Contraseña es muy larga");
        return false;
    }
    else if(!expresion2_password.test(contrasena_validator)){
        alert("Contraseña: Debe contener al menos un numero y una letra mayúscula y minúscula, y al menos 8 caracteres o más");
        return false;
    }
}
*/