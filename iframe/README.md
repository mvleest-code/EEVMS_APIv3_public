## Eagle Eye VMS Iframe Example ##

Add a cameraId to the "src" of the iFrame and the accessToken to "token" within the <script>

````
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>iframe example</title>
  </head>
  <body>
    <iframe 
      id="test-iframe" 
      height="700" 
      width="1000" 
      title="History Browser" 
      src="https://iframe.eagleeyenetworks.com/#/history?ids=<cameraId>"
    ></iframe>
    <script>
      const iframe = document.getElementById("test-iframe").contentWindow;
      window.addEventListener("message", event => {
        if (event.data === 'een-iframe-loaded' || event.data === "een-iframe-token-expired") {
          iframe.postMessage({ 
            type: "een-token", 
            token: "<accesToken>"
          }, "https://iframe.eagleeyenetworks.com/");
        }
      });
    </script>
  </body>
</html>
```