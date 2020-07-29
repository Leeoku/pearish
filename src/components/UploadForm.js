
import React, { useState, useEffect } from "react";
import FileUploadService from "../services/FileUploadService";
const UploadForm=()=>{
    const[selectedFile, setSelectedFile] = useState(undefined);
    const [currentFile, setCurrentFile] = useState(undefined);
    const [progress, setProgress] = useState(0);
    const [message, setMessage] = useState("");
    const [fileInfos, setFileInfos] = useState("");

    const selectFile = (event) => { 
        setSelectedFile(event.target.files);
    };
    const upload = () => {
        let currentFile = selectedFile[0];
        
        setProgress(0);
        setCurrentFile(currentFile);

        FileUploadService.upload(currentFile,(event) =>{
            
        })
        // .then((response)=>{
        //     setMessage(response.data.message);
        //     return FileUploadService.getFiles();
        // })
        .then((files)=>{
            setFileInfos(files.data);
        })
        .catch(()=>{
            setProgress(0);
            setMessage("could not upload the file!");
            setCurrentFile(undefined);
        });
        setSelectedFile(undefined);
    };
    // useEffect(()=>{
    //    FileUploadService.getFiles().then((response)=>{
    //        setFileInfos(response.data);
    //    });
    // }, []);
return(<div>
    {currentFile && (
      <div className="progress">
        <div
          className="progress-bar progress-bar-info progress-bar-striped"
          role="progressbar"
          aria-valuenow={progress}
          aria-valuemin="0"
          aria-valuemax="100"
          style={{ width: progress + "%" }}
        >
          {progress}%
        </div>
      </div>
    )}

    <label className="btn btn-default">
      <input type="file" onChange={selectFile} />
    </label>

    <button
      className="btn btn-success"
      disabled={!selectedFile}
      onClick={upload}
    >
      Upload
    </button>

    <div className="alert alert-light" role="alert">
      {message}
    </div>

    <div className="card">
      <div className="card-header">List of Files</div>
      <ul className="list-group list-group-flush">
        {/* {fileInfos &&
          fileInfos.map((file, index) => (
            <li className="list-group-item" key={index}>
              <a href={file.url}>{file.name}</a>
            </li>
          ))} */}
      </ul>
    </div>
  </div>
  )
};
export default UploadForm;