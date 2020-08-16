//Validar Campos
(function () {
   'use strict';
   window.addEventListener('load', function () {
       // Fetch all the forms we want to apply custom Bootstrap validation styles to
       var forms = document.getElementsByClassName('form-horizontal');
       // Loop over them and prevent submission
       var validation = Array.prototype.filter.call(forms, function (form) {
           form.addEventListener('submit', function (event) {
               if (form.checkValidity() === false) {
                   event.preventDefault();
                   event.stopPropagation();
               }
               form.classList.add('was-validated');
           }, false);
       });
   }, false);
})();


$(document).ready(function ($) {
//  var url_base = "http://localhost:8000/";
  var url_base = "https://sigalogs.herokuapp.com/";
//   var urlCEP = "https://viacep.com.br/ws/"

   if ($("#login-alerta").html() === "") {
       $("#login-alerta").hide();
   } else {
       $("#login-alerta").show();
   };

   // exibe alerta regsitro
   if ($("#registro-alerta").html() === "") {
       $("#registro-alerta").hide();
   } else {
       $("#registro-alerta").show();
   };

   // exibe alerta envioemail
   if ($("#recupera-senha").html() === "") {
       $("#recupera-senha").hide();
   } else {
       $("#recupera-senha").show();
   };

   $('#dataTableSistemas').DataTable({
        "order": [[2, "asc"]]
   });


   $("#btn-dados").click(function(){
       $("#paneDados").show();
       $("#paneSenha").hide();
       $("#paneMenu").hide();
   });
   
   $("#btn-senha").click(function(){
       $("#paneDados").hide();
       $("#paneSenha").show();
       $("#paneMenu").hide();        
   });

   $("#btnSalvarDados").click(function(){
       if (validarDados()){
           $.ajax({
               type: "POST",
               url: url_base + "perfil/atualizar",
               data:{id: $("#id").val(), 
                     email:$("#email").val(),   
                     nomecompleto: $("#nomecompleto").val(),
                     celular: $("#celular").val(),
                     dtnascimento: $("#dtnascimento").val(),
                     sexo: $("#sexo").val()
                    },
               async: false,
               success: function (data) { 
                   $(location).attr('href', url_base + 'perfil');
               }
           });     
       }        
   });

   $("#btnSalvarSistema").click(function(){
       if (validarSistema()){
           $.ajax({
               type: "POST",
               url: url_base + "sistemas/registrar",
               data:{id: $("#id").val(), 
                     dtregistro:$("#dtregistro").val(),   
                     nome:$("#nome").val(),   
                     descricao: $("#descricao").val(),
                     tipo: $("#tipo").val(),
                     linguagem: $("#linguagem").val()
                    },
               async: false,
               success: function (data) { 
                   var itens =  data.split(",");                       
                   alert(itens[1]);
                //    var t = JSON.parse(data);                   
                //    if(data['code']==='200'){
                //         $(location).attr('href', url_base + 'sistemas');
                //    }
                //    else{      
                //         var result = JSON.parse(data.msg);
                //         var msgs =  result.message.split(",");                       
                //         str = "<ul>";
                //         for(i=0;i<msgs.length-1; i++){
                //             str += "<p>" + msgs[i].replace("[", "").replace("]", "") + "</p>";                            
                //         }
                //         str += "</ul>";
                //         $("#registro-alerta").html(str);
                //         $("#registro-alerta").show();                 
                //    }
               }
           });     
       }        
   });

   // $("#btnSalvarSenha").click(function(){
   //     if(validarSenha()){
   //         $.ajax({
   //             type: "POST",
   //             url: url_base + "perfil/acesso",
   //             data:{senhaAtual: $("#senhaAtual").val(), senha: $("#senha").val()},
   //             async: false,
   //             success: function (data) {
   //                 if (data==="403"){
   //                     bootbox.alert({
   //                         message: "Senha atual não confere!",
   //                         size: 'small'
   //                     });                        
   //                     $("#senhaAtual").focus();                        
   //                 }
   //                 else{
   //                     bootbox.alert({
   //                         message: "Senha alterada com sucesso!",
   //                         size: 'small'
   //                     });                        
   //                     $("#senhaAtual").val("");
   //                     $("#senha").val(""),
   //                     $("#resenha").val("");
   //                 }
   //             }
   //         });     
   //     }        
   // });
   $("#btn-signup").click(function () {
       if (validar()) {
           $.ajax({
               type: "POST",
               url: url_base + "registro/envio",
               data:{nomecompleto: $("#nomecompleto").val(),
                   email: $("#email").val(),
                   celular: $("#celular").val(),
                   dtnascimento: $("#dtnascimento").val(),
                   sexo: $("#sexo").val(),
                   senha: $("#senha").val()
                   },
               async: false,
               success: function (data) { 
                   bootbox.alert({
                       message: "Registro efetuado com sucesso",
                       size: 'small'
                   });    

                   $("#nomecompleto").val("");
                   $("#email").val("");
                   $("#celular").val("");
                   $("#dtnascimento").val("");
                   $("#sexo").val("Sexo *");
                   $("#senha").val("");
                   $("#resenha").val("");
               }
           });            
       }
   });


   // functions
   function validaremail() {
       var msg = "O campo deve ser informado!"

       if ($("#email-recuperar").val().trim().length === 0) {
           $("#recupera-senha").html(msg);
           $("#recupera-senha").show();
           $("#email-recuperar").focus();
           return false;
       }

       if (!validateEmail($("#email-recuperar").val())) {
           $("#recupera-senha").html("Email não esta no formato válido!");
           $("#recupera-senha").show();
           $("#email-recuperar").focus();
           return false;
       }
       return true;
   }


   function validateEmail(email) {
       var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
       return re.test(String(email).toLowerCase());
   }

   function email_exist(email) {
       $.get("validaremail/" + email,
           function (result) {
               if (result === "404") {
                   $("#registro-alerta").html("Ops! Esse email já esta sendo utilizado por outro usuário!");
                   $("#registro-alerta").show();
                   $("#email").focus();
                   return true;
               };
               return false;
           });
   }

   function celular_exist(celular) {
       $.get("validarfone/" + celular,
           function (result) {
               if (result === "404") {
                   $("#registro-alerta").html("Ops! Esse telefone celular já esta sendo utilizado por outro usuário!");
                   $("#registro-alerta").show();
                   $("#celular").focus();
                   return true;
               };
               return false;
           });
   }


   function validarSenha(){
       var msg = "O campo deve ser informado!"        

       if ($("#senhaAtual").val().trim().length == 0) {
           $("#registro-alerta-senha").html(msg);
           $("#registro-alerta-senha").show();
           $("#senhaAtual").focus();
           return false;
       }

       if ($("#senha").val().trim().length == 0) {
           $("#registro-alerta-senha").html(msg);
           $("#registro-alerta-senha").show();
           $("#senha").focus();
           return false;
       }
       if ($("#senha").val().trim().length < 5) {
           $("#registro-alerta-senha").html("A senha informada deve ter ao menos 5 caracteres");
           $("#registro-alerta-senha").show();
           $("#senha").focus();
           return false;
       }
       if ($("#resenha").val().trim().length == 0) {
           $("#registro-alerta-senha").html(msg);
           $("#registro-alerta-senha").show();
           $("#resenha").focus();
           return false;
       }
       if ($("#senha").val().trim() != $("#resenha").val().trim()) {
           $("#registro-alerta-senha").html("O valor não confere com a senha informada");
           $("#registro-alerta-senha").show();
           $("#resenha").focus();
           return false;
       }

      return true;

   }

   function validarSistema(){
        var msg = "O campo deve ser informado!"

        if ($("#nome").val().trim().length === 0) {
            $("#registro-alerta").html(msg);
            $("#registro-alerta").show();
            $("#nome").focus();
            return false;
        }

        if ($("#descricao").val().trim().length == 0) {
            $("#registro-alerta").html(msg);
            $("#registro-alerta").show();
            $("#descricao").focus();
            return false;
        }

        if ($("#tipo").val() === "Tipo *") {
            $("#registro-alerta").html(msg);
            $("#registro-alerta").show();
            $("#tipo").focus();
            return false;
        }

        if ($("#linguagem").val().trim().length == 0) {
            $("#registro-alerta").html(msg);
            $("#registro-alerta").show();
            $("#linguagem").focus();
            return false;
        }

        return true;
   }


   function validarDados() {
       var msg = "O campo deve ser informado!"

       if ($("#nomecompleto").val().trim().length === 0) {
           $("#registro-alerta").html(msg);
           $("#registro-alerta").show();
           $("#nomecompleto").focus();
           return false;
       }

       if ($("#celular").val().trim().length === 0 || $("#celular").val().trim() === "() -") {
           $("#registro-alerta").html(msg);
           $("#registro-alerta").show();
           $("#celular").focus();
           return false;
       }

       if ($("#dtnascimento").val().trim().length == 0) {
           $("#registro-alerta").html(msg);
           $("#registro-alerta").show();
           $("#dtnascimento").focus();
           return false;
       }

       if ($("#sexo").val() === "Sexo *") {
           $("#registro-alerta").html(msg);
           $("#registro-alerta").show();
           $("#sexo").focus();
           return false;
       }

       return true;
   }


   function validar() {
       var msg = "O campo deve ser informado!"

       if ($("#nomecompleto").val().trim().length === 0) {
           $("#registro-alerta").html(msg);
           $("#registro-alerta").show();
           $("#nomecompleto").focus();
           return false;
       }

       if ($("#email").val().trim().length === 0) {
           $("#registro-alerta").html(msg);
           $("#registro-alerta").show();
           $("#email").focus();
           return false;
       }

       if (!validateEmail($("#email").val())) {
           $("#registro-alerta").html("Email não esta no formato válido!");
           $("#registro-alerta").show();
           $("#email").focus();
           return false;
       }

       if ($("#celular").val().trim().length === 0 || $("#celular").val().trim() === "() -") {
           $("#registro-alerta").html(msg);
           $("#registro-alerta").show();
           $("#celular").focus();
           return false;
       }

       if (celular_exist($("#celular").val())) {
           return false;
       }

       if (email_exist($("#email").val())) {
           return false;
       }

       if ($("#dtnascimento").val().trim().length == 0) {
           $("#registro-alerta").html(msg);
           $("#registro-alerta").show();
           $("#dtnascimento").focus();
           return false;
       }

       if ($("#sexo").val() === "Sexo *") {
           $("#registro-alerta").html(msg);
           $("#registro-alerta").show();
           $("#sexo").focus();
           return false;
       }
       if ($("#senha").val().trim().length == 0) {
           $("#registro-alerta").html(msg);
           $("#registro-alerta").show();
           $("#senha").focus();
           return false;
       }
       if ($("#senha").val().trim().length < 5) {
           $("#registro-alerta").html("A senha informada deve ter ao menos 5 caracteres");
           $("#registro-alerta").show();
           $("#senha").focus();
           return false;
       }
       if ($("#resenha").val().trim().length == 0) {
           $("#registro-alerta").html(msg);
           $("#registro-alerta").show();
           $("#resenha").focus();
           return false;
       }
       if ($("#senha").val().trim() != $("#resenha").val().trim()) {
           $("#registro-alerta").html("O valor não confere com a senha informada");
           $("#registro-alerta").show();
           $("#resenha").focus();
           return false;
       }

       return true;
   }
});