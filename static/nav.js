function logout(){
    $.removeCookie('token');
    alert("로그아웃")
    window.location.reload()
}

 $(function() {
    let name = $('h1').attr('class');
    console.log(name)
    if(name==""){
         $('#join').show()
        $('#login').show()
        $('#logout').hide()
    } else{
         $('#join').hide()
        $('#login').hide()
    }


   })
