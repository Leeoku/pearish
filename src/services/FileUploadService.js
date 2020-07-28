import axios from "axios";

const upload = (file, onUploadProgress)=>{
    let formData = new FormData();
    
    formData.append("file", file);

    return axios.post("users/upload", formData, {
        headers:{
            "Content-type" : "multipart/form-data",
        },
        onUploadProgress,
    });
};
const getFiles=()=>{
    return axios.get("/files");
};

export default{
    upload,
    getFiles,
};