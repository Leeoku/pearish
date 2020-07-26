import React, { useRef,useState } from "react";
import Axios from "axios";
const UploadForm=()=>{
    const[selectedFile, setSelectedFile] = useState(null);
    const form = useRef(null)
    const onSubmitHandler = (e) => {
        e.preventDefault()
        const data = new FormData (form.current)
        data.append('file', selectedFile)
        Axios.post("/user/upload", data,{
            headers:{
                'Content-Type': 'multipart/form-data'
            }
        }).then(res=>{console.log(res.statusText("axios"))})
    }
    const onChangeHandler = (e) =>{
        setSelectedFile(e.target.files[0])
        console.log(e.target.files[0])
      }
return(
    <div className= "container">
        <form className = "form"
        onSubmit={onSubmitHandler}>
            <div>
            <input 
            accept ="image/*"
            type = "file" 
            name="file" 
            value = {selectedFile}
            onChange={onChangeHandler}/>
            </div>
            <button type= "submit">Upload a receipt</button>
        </form>
    </div>
  )
}
export default UploadForm;