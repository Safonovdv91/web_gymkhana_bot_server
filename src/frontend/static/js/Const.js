const AppConsts = {

  "EnvName" = "Dev",
  "LocalBaseUrl" = "http://127.0.0.1:8000",
  "ProdBaseUrl" = "https://rabbitmg.ru/",
  "BaseUrl" = "__BaseUrl__"  
};

function init(){
  if(AppConsts.EnvName == "Dev")
  {
    AppConsts.BaseUrl = AppConsts.LocalBaseUrl;
  }
  else{
    AppConsts.BaseUrl = AppConsts.ProdBaseUrl;
  }
}
