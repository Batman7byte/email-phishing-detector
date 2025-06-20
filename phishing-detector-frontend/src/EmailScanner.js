import React, { useState, useEffect } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import './styles.css'; // Import the CSS styles

const EmailScanner = () => {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [selectedEmails, setSelectedEmails] = useState([]);

  const fetchEmails = async () => {
    setLoading(true);
    try {
      const response = await axios.get("http://localhost:5000/emails");
      setEmails(response.data);
      toast.success("Emails updated!");
    } catch (error) {
      console.error("Error fetching emails:", error);
      toast.error("Failed to fetch emails");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmails();
    if (autoRefresh) {
      const interval = setInterval(fetchEmails, 10000);
      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  const handleSelectEmail = (id) => {
    setSelectedEmails((prev) =>
      prev.includes(id) ? prev.filter((emailId) => emailId !== id) : [...prev, id]
    );
  };

  const deleteSelectedEmails = async () => {
    if (selectedEmails.length === 0) {
      toast.warn("No emails selected!");
      return;
    }
    try {
      await axios.post("http://localhost:5000/delete_emails", { email_ids: selectedEmails });
      toast.success("Selected emails deleted!");
      setEmails((prev) => prev.filter((email) => !selectedEmails.includes(email.id)));
      setSelectedEmails([]);
    } catch (error) {
      console.error("Error deleting emails:", error);
      toast.error("Failed to delete emails");
    }
  };

  return (
    <div className="container mx-auto p-6">
      <center><h1 className="text-3xl font-bold mb-4 neon text-center">📧 PHISHING DETECTOR AI</h1></center>

     <div className="flex justify-center gap-4 mb-8">
  <button
    onClick={fetchEmails}
    className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
    disabled={loading}
  >
    {loading ? "Refreshing..." : "🔄 Refresh Emails"}
  </button>
  <button
    onClick={() => setAutoRefresh(!autoRefresh)}
    className={`px-4 py-2 rounded ${autoRefresh ? "bg-red-500" : "bg-green-500"} text-white hover:opacity-80`}
  >
    {autoRefresh ? "⛔ Stop Auto-Refresh" : "✅ Start Auto-Refresh"}
  </button>
  <button
    onClick={deleteSelectedEmails}
    className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
  >
    🗑️ Delete Selected Emails
  </button>
</div>


      {loading && <p className="text-gray-500 text-center">Loading emails...</p>}
      {emails.length === 0 && !loading && <p className="text-gray-500 text-center">No emails found.</p>}

      {emails.length > 0 && (
        <table className="mt-4 w-full border-collapse border border-gray-300 table">
          <thead>
            <tr className="bg-gray-200">
              <th className="border p-2">Select</th>
              <th className="border p-2">ID</th>
              <th className="border p-2">Detailed Information</th>
              <th className="border p-2">Phishing?</th>
            </tr>
          </thead>
          <tbody>
            {emails.map((email) => (
              <tr key={email.id} className="border">
                <td className="border p-2 text-center">
                  <input
                    type="checkbox"
                    checked={selectedEmails.includes(email.id)}
                    onChange={() => handleSelectEmail(email.id)}
                  />
                </td>
                <td className="border p-2">{email.id}</td>
                <td className="border p-2">{email.snippet}</td>
                <td
                  className={`border p-2 text-white font-bold ${
                    email.is_phishing ? "bg-red-500" : "bg-green-500"
                  }`}
                >
                  {email.is_phishing ? "🚨 Yes (Phishing)" : "✅ No (Safe)"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <ToastContainer />
    </div>
  );
};

export default EmailScanner;