import React, { useState } from "react";
const UploadForm=()=>{
    const[selectedFile, setSelectedFile] = useState("");
    const onChangeHandler = (e) =>{
        setSelectedFile(e.target.files[0])
        console.log(e.target.files[0])
      }
return(
    <div className= "container">
        <form className = "form"
        onSubmit={(e) => e.preventDefault()}>
            <div>
            <input 
            accept = "image/*"
            type = "file" 
            name="file" 
            value = {selectedFile}
            onChange={onChangeHandler}/>
            </div>
        </form>
    </div>
  )
}
export default UploadForm;