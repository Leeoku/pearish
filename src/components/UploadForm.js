import React, { useState} from "react";
import FileUploadService from "../services/FileUploadService";

const UploadForm = (props) => {
  const [selectedFile, setSelectedFile] = useState(undefined);
  const [currentFile, setCurrentFile] = useState(undefined);
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState("");
  const [setFileInfos] = useState("");

  const selectFile = (event) => {
    setSelectedFile(event.target.files);
  };
  const upload = () => {
    let currentFile = selectedFile[0];

    setProgress(0);
    setCurrentFile(currentFile);

    FileUploadService.upload(currentFile, (event) => {}, props.email)
      .then((files) => {
        setFileInfos(files.data);
        setMessage("Filed Uploaded!");
      })
      .catch(() => {
        setProgress(0);
        setMessage("could not upload the file!");
        setCurrentFile(undefined);
      });
    setSelectedFile(undefined);
  };
  return (
    <div>
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
        <div><span>Image must be less than 1 MB </span></div>
      <div className="alert alert-light" role="alert">
        {message}
      </div>

      <div className="card">
      </div>
    </div>
  );
};
export default UploadForm;
