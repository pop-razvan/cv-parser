"use client";

import { useState } from "react";

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  // Update state when a file is selected
  const handleFileChange = (e: any) => {
    setFile(e.target.files[0]);
  };

  // Handle form submission
  const handleSubmit = async (e: any) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a PDF file to upload.");
      return;
    }

    // Create a FormData object and append the file
    const formData = new FormData();
    formData.append("pdf", file);

    try {
      // Send the file to our API endpoint
      const res = await fetch("http://127.0.0.1:5000/api/upload", {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        const data = await res.json();
        setMessage(data.message || "File uploaded successfully!");
      } else {
        setMessage("File upload failed.");
      }
    } catch (error) {
      console.error("Upload error:", error);
      setMessage("An error occurred during file upload.");
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Upload a PDF File</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
        />
        <button type="submit" style={{ marginLeft: "1rem" }}>
          Upload
        </button>
      </form>
      {message && <p style={{ marginTop: "1rem" }}>{message}</p>}
    </div>
  );
}
