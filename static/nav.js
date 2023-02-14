function logout(){
    $.removeCookie('token');
    alert("로그아웃")
    window.location.reload()
}

 $(function() {
    let name = $('h1').attr('class');
    let token = document.cookie
    console.log(token)
    if(token===""||token===undefined||token===null){
        $('#join').show()
        $('#login').show()
        $('#logout').hide()
    } else{
        $('#join').hide()
        $('#login').hide()
    }


   })
