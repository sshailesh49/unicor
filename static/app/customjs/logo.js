var url_site='http://127.0.0.1:8000/'
$(document).ready(function(){
      
        
        logoData();
        
        
        
       
       
});
  function logoData()
  {
    
       $.ajax({
            url: url_site+'LogoAppAPI/',
            type: 'get',
            //headers: {"Authorization": AUTH_TOKEN},
            dataType: 'json',
            success: function(data, textStatus, xhr)
              {
              
              
          
                
            
                var logo = '';
                
                for(var i=0;i<data.length;i++)
                { 
                  $("img#logoimage").attr('src',data[i].logoImage)
                  
                 }
              
                
                }

           
          });
  };
