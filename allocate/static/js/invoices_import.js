var inputType = document.querySelector(".input-type");
var loadFromFile = document.getElementById("load-from-file");
var loadFromGDrive = document.getElementById("load-from-gdrive");

function loadFromFileFunc(){

    inputType.innerHTML = `
    <form method="POST" action="" id="local-input-form" enctype="multipart/form-data">
        <div class="mb-3">
            <label for="formFileMultiple" class="form-label">Wczytaj pliki z lokalnego dysku</label>
            <input class="form-control" type="file" name="formFileMultiple" id="formFileMultiple" accept=".pdf,.jpg,.png" multiple />
        </div>
        <button type="submit" class="btn btn-dark">Wczytaj</button>
    </form>
    `

};

loadFromFile.addEventListener("click",loadFromFileFunc);