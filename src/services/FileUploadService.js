import axios from "axios";
import Profile from "../components/Profile";

const upload = (file, onUploadProgress, email)=>{
    let formData = new FormData();
    formData.append("file", file);
    // <Profile value = {this.state.email} />
    // user_email = this.props.value
    // return axios.post("http://localhost:5000/users/upload", formData, {
    //     headers:{
    //         "Content-type" : "multipart/form-data",
    //     },
    //     onUploadProgress,
    // });
    return axios.all([
        axios.post("http://localhost:5000/users/upload", formData, {
        headers:{
            "Content-type" : "multipart/form-data",
        },
        onUploadProgress,
    }),
        axios.post("http://localhost:5000/users/"+ email+"/items")
    ])

};
// const getFiles=()=>{
//     return axios.get("/files");
// };

export default{
    upload,
    // getFiles,
};