import axios from "axios";
// import Profile from "../components/Profile";


const upload = (file, onUploadProgress, email)=>{
    let formData = new FormData();
    formData.append("file", file);
    // return axios.post("http://localhost:5000/users/upload", formData, {
    //     headers:{
    //         "Content-type" : "multipart/form-data",
    //     },
    //     onUploadProgress,
    // });
    return axios.all([
        axios.post("/users/upload", formData, {
        headers:{
            "Content-type" : "multipart/form-data",
        },
        onUploadProgress,
    }),
        axios.post("/users/" + encodeURIComponent(email) + "/items",{
        headers:{
            "Content-type" : "text/html; charset=UTF-8", 
        }}),
    ])

};

export default{
    upload,
    // getFiles,
};