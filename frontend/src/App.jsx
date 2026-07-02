import { useState } from "react";
import UploadExcel from "./components/UploadExcel";
import UploadInvoice from "./components/UploadInvoice";
import ResultCard from "./components/ResultCard";

function App() {
  const [invoice, setInvoice] = useState(null);

  return (
    <div className="container">

      <h1>📄 AI Invoice Parser</h1>

      <UploadExcel />

      <UploadInvoice setInvoice={setInvoice} />

      {invoice && <ResultCard invoice={invoice} />}

    </div>
  );
}

export default App;