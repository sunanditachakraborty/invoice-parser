import { useState } from "react";
import api from "../api";

export default function UploadInvoice({ setInvoice }) {

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const upload = async () => {

    if (!file) {
      alert("Choose an invoice.");
      return;
    }

    const data = new FormData();
    data.append("file", file);

    try {

      setLoading(true);

      const response = await api.post(
        "/upload-invoice",
        data
      );

      setInvoice(response.data.invoice);

    } catch (err) {

      alert(err.response?.data?.detail || "Extraction failed");

    } finally {

      setLoading(false);

    }

  };

  return (

    <div className="card">

      <h2>Upload Invoice</h2>

      <input
        type="file"
        accept="image/*,.pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button
        disabled={loading}
        onClick={upload}
      >
        {loading ? "Extracting..." : "Extract Invoice"}
      </button>

    </div>

  );
}