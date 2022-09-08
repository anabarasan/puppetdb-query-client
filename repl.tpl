<!doctype html>
<html>
  <body>
    <form method="post">
      <textarea style="width:100%; height:100px;" id="txt_query" name="txt_query">{{query}}</textarea>
      <input style="width:100%;" type="submit" id="btn_execute" name="btn_execute" value="Execute"/>
    </form>
    %if "error" in result and result["error"]:
    <div id="error_msg">
      <pre style="color:crimson;">
        {{result["error_msg"]}}
      </pre>
    </div>
    %else:
      %if "output" in result:
      <div id="json-input" style="margin-top:10px;">
        {{result["output"]}}
      </div>
      <pre id="json-renderer" class="json-tree" style="margin-top:10px;">
      </pre>
      <input class="path" type="text"/>
      <script>
        const source = document.getElementById("json-input");
        const dest = document.getElementById("json-renderer");
        const pretty_json = JSON.stringify(JSON.parse(source.innerHTML), null, 2);
        dest.innerHTML = pretty_json;
        source.style.display = "none";
      </script>
      %end
    %end
  </body>
</html>
