import React from "react";
const UploadForm=()=>{
    const[selectedFile, setSelectedFile] = ("");
    const onSubmitHandler = (e) => { 
        e.preventDefault()
    }
    const onChangeHandler = (e) =>{
        setSelectedFile(e.target.files[0])
        console.log(e.target.files[0])
      }
return(
    <div className= "container">
        <form className = "form"
        onSubmit = {onSubmitHandler}>
            <div>
            <input 
            type = "file" 
            name="file" 
            onChange={onChangeHandler}/>
            </div>
        </form>
    </div>
  )
}
export default UploadForm;