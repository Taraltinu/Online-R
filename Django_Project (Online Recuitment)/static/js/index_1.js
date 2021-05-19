// Filter By Job Type
    $('.remotely').click(function(){
    var catid;
    catid = $('#remote').text();
    console.log(catid)
    $.ajax(
    {
        type:"GET",
        url: "/",
        data:{
                 post_id: catid
        },
        success: function( data ) 
        {
            $( '#like'+ catid ).remove();
            $( '#message' ).text(data);
        }
     })
});
