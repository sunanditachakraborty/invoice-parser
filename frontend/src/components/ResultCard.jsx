export default function ResultCard({ invoice }) {

  return (

    <div className="card">

      <h2>Extracted Information</h2>

      <table>

        <tbody>

          {Object.entries(invoice).map(([key, value]) => (

            <tr key={key}>
              <td><strong>{key}</strong></td>
              <td>{value || "-"}</td>
            </tr>

          ))}

        </tbody>

      </table>

      <br />

      <a
        href="http://127.0.0.1:8000/download-excel"
        target="_blank"
        rel="noreferrer"
      >
        <button>
          Download Updated Excel
        </button>
      </a>

    </div>

  );
}