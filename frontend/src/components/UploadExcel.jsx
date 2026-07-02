import { useState } from "react";
import api from "../api";

export default function UploadExcel() {

  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const upload = async () => {

    if (!file) {
      alert("Choose an Excel workbook.");
      return;
    }

    const data = new FormData();
    data.append("file", file);

    try {
      await api.post("/upload-excel", data);

      setStatus("✅ Workbook uploaded successfully");
    } catch (err) {
      setStatus("❌ Upload failed");
    }
  };

  return (
    <div className="card">

      <h2>Upload Workbook</h2>

      <input
        type="file"
        accept=".xlsx"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={upload}>
        Upload Excel
      </button>

      <p>{status}</p>

    </div>
  );
}