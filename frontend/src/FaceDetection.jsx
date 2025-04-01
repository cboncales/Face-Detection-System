import { useState } from "react";
import axios from "axios";

const FaceDetection = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imageUrl, setImageUrl] = useState("");

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/upload",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      setImageUrl(`http://127.0.0.1:5000/processed/${response.data.filename}`);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="max-w-lg mx-auto mt-10 bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold text-center text-gray-700 mb-4">
        Face Detection System
      </h2>

      <div className="flex flex-col items-center space-y-4">
        <input
          type="file"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-500 
                 file:mr-4 file:py-2 file:px-4 
                 file:rounded-lg file:border-0 
                 file:text-sm file:font-semibold 
                 file:bg-blue-500 file:text-white 
                 hover:file:bg-blue-600 cursor-pointer"
        />

        <button
          onClick={handleUpload}
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg font-medium 
                 hover:bg-blue-600 transition duration-300"
        >
          Upload & Detect Faces
        </button>
      </div>

      {imageUrl && (
        <div className="mt-6 text-center">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">
            Processed Image
          </h3>
          <div className="border rounded-lg p-2 shadow-md inline-block">
            <img
              src={imageUrl}
              alt="Processed Face Detection"
              className="max-w-full rounded-lg"
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default FaceDetection;
