// document.getElementById('addInstructionButton').addEventListener('click', function() {
//     // Select the HTML container
//     var instruction = document.getElementById('instruction');

//     // Create a copy of the container
//     var containerClone = instruction.cloneNode(true);

//     // Append the container copy to the body (you can append it to another element if needed)
//     parentInstruction.appendChild(containerClone);
// });


var instructionCount = 1;

  document.getElementById('addInstructionButton').addEventListener('click', function(event) {
    // Prevent default submission
    event.preventDefault()

    // Increment the count
    instructionCount++;

    // Create a new instruction div
    var newInstructionDiv = document.createElement('div');
    newInstructionDiv.className = 'row';
    newInstructionDiv.id = 'instruction' + instructionCount;
    newInstructionDiv.name = 'instruction' + instructionCount;

    // Add content to the new instruction div
    newInstructionDiv.innerHTML = `
    <div class="container px-3 py-2 post-instruction-title rounded-top text-white" style="background-color: #F06205; height: 70px;">
            <div class="row align-items-center">
                    <!-- INSTRUCTION -->
                    <div class="col post-instruction">
                        <div class="form-floating">
                            <textarea class="form-control" name="instructionTitle" id="instructionTitle" style="background-color: #F06205; border: 0px"></textarea>
                            <label for="instructionTitle">Instruction</label>
                        </div>
                    </div>
                    <div class="col-1 d-flex justify-content-center">
                        <div class="btn text-white" onclick="removeInstruction('instruction${instructionCount}')" style="font-size: 30px;">
                            &times;
                        </div>
                    </div>
                </div>
            </div>
        
        <div class="container py-4" style="background-color: white;">
            <!-- IMG -->
            <div class="row">
                    <div class="container d-flex align-items-center justify-content-center mb-3" style="background-color: rgb(223, 223, 223); height: 450px; ">
                        <div class="text-center">   
                            <label class="text-center" for="pic">
                                <p class="h1" style="font-family: 'Lato', sans-serif; font-weight: bold; font-size: 45px; color: #7E7E7E; margin-bottom: 20px;">
                                [Display Image Here]
                                </p>
                                <span class="material-icons" style="font-size: 48px; margin-top: 20px; cursor: pointer; color: gray;">
                                add_photo_alternate
                                </span>
                            </label>
                        </div>
                    </div>
                    <br>
                    <input type="file" name="pic" id="pic" style="display: none;"/>

                    <script>
                        document.getElementById('imageForm').addEventListener('click', function() {
                            document.getElementById('imageUpload').click();
                        });
                
                        document.getElementById('imageUpload').addEventListener('change', function() {
                            var uploadedImage = document.getElementById('uploadedImage');
                            var uploadLabel = document.getElementById('uploadLabel');
                            var imageIcon = document.getElementById('imageIcon');
                            var fileInput = document.getElementById('imageUpload');
                            var file = fileInput.files[0];
                            var reader = new FileReader();
                
                            reader.onload = function(e) {
                                uploadedImage.src = e.target.result;
                                uploadedImage.style.display = 'block';
                                uploadLabel.style.display = 'none';
                                imageIcon.style.display = 'none';
                            };
                
                            reader.readAsDataURL(file);
                        });
                
                        document.getElementById('uploadedImage').addEventListener('click', function() {
                            document.getElementById('imageUpload').click();
                        });
                    </script>

                </div>

            <!-- IMG DESCRIPTION -->
            <div class="row pt-2 px-4">
                <div class="form-floating">
                    <textarea class="form-control px-4" placeholder="Leave a comment here" id="floatingTextarea2" style="height: 100px"></textarea>
                    <label class="ms-4" for="floatingTextarea2">Add description here...</label>
                </div>
            </div>
            
        </div>
        <hr>  
    
    `;

    // Append the new instruction div to the parent
    document.getElementById('parentInstruction').appendChild(newInstructionDiv);
  });

  function removeInstruction(instructionId) {
    var instructionDiv = document.getElementById(instructionId);
    instructionDiv.parentNode.removeChild(instructionDiv);
  }