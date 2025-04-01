import React from "react";
import FaceDetection from "./FaceDetection";

const App = () => {
  return (
    <div className="bg-gray-500">
      <h1 className="text-2xl font-semibold text-gray-100 mb-4">
        Face Detection App
      </h1>
      <FaceDetection />
    </div>
  );
};

export default App;
