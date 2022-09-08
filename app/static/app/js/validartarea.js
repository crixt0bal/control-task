function validarregister(){
    var nombre_usuario, email, password, expresion, expresion2;
    nombre_usuario = document.getElementById("nombre_usuario").value;
    email = document.getElementById("email").value;
    password = document.getElementById("password").value;

    

    expresion = /^([\da-z_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/;
    expresion2 = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
    



    if(nombre_usuario === "" || email === "" || password === ""){
        alert("Todos los campos son obligatorios");
        return false;

    }
    else if(nombre_usuario.length>50){
        alert("El nombre de usuario es muy largo");
        return false;
    }
    else if(email.length>100){
        alert("El correo es muy largo");
        return false;
    }
    else if(!expresion.test(email)){
        alert("El correo no es valido");
        return false;
    }
    else if(password.length>300){
        alert("La Contraseña es muy larga");
        return false;
    }
    else if(!expresion2.test(password)){
        alert("Contraseña: Debe contener al menos un numero y una letra mayúscula y minúscula, y al menos 8 caracteres o más");
        return false;
    }
}