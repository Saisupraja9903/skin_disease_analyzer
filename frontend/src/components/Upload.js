// import React, { useState, useEffect, useRef } from "react";
// import ReactMarkdown from "react-markdown";
// import remarkGfm from "remark-gfm";
// import axios from "axios";
// import html2canvas from "html2canvas";
// import jsPDF from "jspdf";
// // import Footer from "./Footer";
// import "./Upload.css";

// function Upload() {
//   const [file, setFile] = useState(null);
//   const [preview, setPreview] = useState(null);
//   const [location, setLocation] = useState(""); // Store user-entered location
//   const [result, setResult] = useState("");
//   const [backendStatus, setBackendStatus] = useState("Checking Server Status...");
//   const [questions, setQuestions] = useState([]); // Stores symptom questions
//   const [answers, setAnswers] = useState({}); // Stores user responses
//   const [awaitingSymptoms, setAwaitingSymptoms] = useState(false); // Waiting for symptom input
//   const [finalReport, setFinalReport] = useState(null); // Stores full AI-generated report
//   const [isSubmitted, setIsSubmitted] = useState(false);
//   const [isOutputReady, setIsOutputReady] = useState(false);
//   const [isSubmitting, setIsSubmitting] = useState(false); // Tracks button loading state
//   const outputRef = useRef(null);
//   const [isUploading, setIsUploading] = useState(false); // Tracks Submit button loading state
//   // const BASE_URL = process.env.REACT_APP_BACKEND_API_URL;
//   const BASE_URL = "http://127.0.0.1:8080";
  
//   axios.get(`${BASE_URL}/api/status`)

//   useEffect(() => {
//     // Simulate output completion
//     setTimeout(() => setIsOutputReady(true), 2000); // Adjust based on real output loading time
//   }, []);

//   const checkBackendStatus = async () => {
//     try {
//       const response = await axios.get(`${BASE_URL}/api/status`); // or '/status'
//       if (response.status === 200) {
//         setBackendStatus("Server Status: Online ✅");
//       } else {
//         setBackendStatus("Server Status: Unknown ❓");
//       }
//     } catch (error) {
//       console.error("Error connecting to backend:", error);
//       setBackendStatus("Server Status: Offline ❌ . ❗Disclaimer: This is site is for Demo purposes only. Do not use for actual diagnosis❗");
//     }
//   };

//   useEffect(() => {
//   checkBackendStatus();
// }, []);


//   const handleFileChange = (event) => {
//     const selectedFile = event.target.files[0];
//     if (selectedFile) {
//       setFile(selectedFile);
//       setPreview(URL.createObjectURL(selectedFile));

//     }
//   };

//   const handleUpload = async () => {
//     if (!file) {
//       alert("Please upload an image.");
//       return;
//     }

//     if (!location.trim()) {
//       alert("Please enter your location.");
//       return;
//     }

//     setIsUploading(true); // Start loading animation

//     const formData = new FormData();
//     formData.append("file", file);
//     formData.append('location', location); // add location too

//     try {
//       const response = await axios.post(`${BASE_URL}/api/upload`, formData, {
//         headers: { "Content-Type": "multipart/form-data" },
//       });

//       if (response.data.questions) {
//         setQuestions(response.data.questions);
//         setAwaitingSymptoms(true);
//         setAnswers({}); // Reset answers
//       } else {
//         setResult(`Disease: ${response.data.disease}, Severity: ${response.data.severity}`);
//       }
//     } catch (error) {
//       console.error("Error uploading file:", error);
//       alert("Error processing image.");
//     } finally {
//       setIsUploading(false); // Stop loading animation
//     }
//   };


//   // ✅ Show alert AFTER `result` updates
//   useEffect(() => {
//     if (result) {
//       alert(result);
//     }
//   }, [result]);


//   const handleAnswerChange = (symptom, value) => {
//     setAnswers(prevAnswers => ({
//       ...prevAnswers,
//       [symptom]: value // Store answer using symptom as key
//     }));
//   };

//   const handleSubmitSymptoms = async () => {
//     if (!location.trim()) {
//       setResult("Please enter your location before submitting symptoms.");
//       return;
//     }

//     setIsSubmitting(true); // Show loading icon

//     try {
//       const response = await axios.post(`${BASE_URL}/api/confirm_symptoms`, { answers });
//       fetchFullDiseaseInfo(response.data.disease, response.data.severity);
//     } catch (error) {
//       console.error("Error confirming symptoms:", error);
//       setResult("Error processing symptoms.");
//       setIsSubmitting(false); // Remove loading if error occurs
//     }
//   };


//   // const fetchFullDiseaseInfo = async (disease, severity) => {
//   //   try {
//   //     console.log(`Sending request for Disease: ${disease}, Severity: ${severity}, Location: ${location}`);

//   //     const response = await axios.post(`${BASE_URL}/api/get_disease_info`, {
//   //       disease,
//   //       severity,
//   //       location,
//   //     });

//   //     setIsSubmitted(true); // Hide "Submit Responses" button after clicking

//   //     // If severity is "Out of Class", set special message & stop further display
//   //     if (response.data.out_of_class) {
//   //       setFinalReport({ outOfClass: true });
//   //       return;
//   //     }

//   //     console.log("Received AI Response:", response.data);
//   //     setFinalReport(response.data);
//   //   } catch (error) {
//   //     console.error("Error fetching disease info:", error.response?.data || error.message);
//   //     setFinalReport({ error: "Failed to retrieve additional details." });
//   //   }
//   // };

//   const fetchFullDiseaseInfo = async (disease, severity) => {
//   try {
//     console.log("📤 Sending:", { disease, severity, location });

//     const response = await axios.post(
//       `${BASE_URL}/api/get_disease_info`,
//       {
//         disease: disease,
//         severity: severity,
//         location: location,
//       }
//     );

//     console.log("📥 Received Full Report:", response.data);

//     setFinalReport(response.data);   // <-- this fills UI

//     setIsSubmitted(true);
//   } catch (error) {
//     console.error("❌ Error fetching disease info:", error);
//     setFinalReport({ error: "Failed to retrieve report" });
//   } finally {
//     setIsSubmitting(false);
//   }
// };



//   const handleDownloadPDF = () => {
//     const element = outputRef.current;

//     html2canvas(element, { scale: 2, useCORS: true }).then((canvas) => {
//       const imgData = canvas.toDataURL("image/png");
//       const pdf = new jsPDF("p", "mm", "a4");

//       const imgWidth = 210; // A4 width in mm
//       const pageHeight = 297; // A4 height in mm  
//       const imgHeight = (canvas.height * imgWidth) / canvas.width;

//       let y = 0; // Position to start adding images

//       while (y < imgHeight) {
//         pdf.addImage(imgData, "PNG", 0, -y, imgWidth, imgHeight);
//         y += pageHeight; // Move to the next page
//         if (y < imgHeight) pdf.addPage(); // Add new page if content is not fully captured
//       }

//       pdf.save("SkinNet_Analyzer_Report.pdf");
//     });
//   };

//   return (
//     <div ref={outputRef} className="upload-container">
//       <p className="backend-status">{backendStatus}</p>
//       {backendStatus === "Checking Server Status..." ? null :
//         backendStatus === "Server Status: Online ✅" ? (
//           <>
//             <div className="title-divv">
//               <h3>❗Disclaimer: This website is for Demonstration Purposes only. Don't use for Real Diagnosis❗</h3>
//               <h1 className="upload-title">Skin Disease Diagnosis</h1>
//             </div>

//             {!preview && (
//               <>
//                 <label htmlFor="file-upload" className="upload-label">Upload Image</label>
//                 <input
//                   id="file-upload"
//                   type="file"
//                   className="upload-input"
//                   accept="image/*"
//                   onChange={handleFileChange}
//                 />
//               </>
//             )}

//             {preview && (
//               <div className="image-preview">
//                 <h3>Image Preview:</h3>
//                 <img src={preview} alt="Selected Preview" className="preview-img" />
//               </div>
//             )}

//             <div className="location-input">
//               <h4 id="location-title">Enter your Location:</h4>
//               <input
//                 id="location-box"
//                 type="text"
//                 placeholder="E.g., Chennai, India"
//                 value={location}
//                 onChange={(e) => setLocation(e.target.value)}
//                 autoComplete="address-level2"
//               />
//             </div>

//             {!awaitingSymptoms ? (
//               <button className="upload-button" onClick={handleUpload} disabled={isUploading}>
//                 {isUploading ? (
//                   <span className="loading-spinner"></span> // Show loading animation
//                 ) : (
//                   "Submit"
//                 )}
//               </button>
//             ) : (
//               <div className="symptom-questions">
//                 <h2>Answer the following questions:</h2>
//                 {questions && Object.entries(questions).map(([symptom, question], index) => (
//                   <div key={index} className="question">
//                     <p>{question}</p>
//                     <button
//                       className={answers[symptom] === "1" ? "selected" : ""}
//                       onClick={() => handleAnswerChange(symptom, "1")}
//                     >
//                       Yes
//                     </button>
//                     <button
//                       className={answers[symptom] === "0" ? "selected" : ""}
//                       onClick={() => handleAnswerChange(symptom, "0")}
//                     >
//                       No
//                     </button>
//                   </div>
//                 ))}
//                 {!isSubmitted && (
//                   <button className="upload-button" onClick={handleSubmitSymptoms} disabled={isSubmitting}>
//                     {isSubmitting ? (
//                       <span className="loading-spinner"></span> // Show loading icon
//                     ) : (
//                       "Submit Responses"
//                     )}
//                   </button>
//                 )}
//               </div>
//             )}

//             {/* If "Out of Class", display only the message */}
//             {finalReport?.outOfClass ? (
//               <h2 className="error-message">Disease Out of Class</h2>
//             ) : finalReport && (
//               <div className="disease-report">
//                 <h2>Diagnosed Disease</h2>
//                 <p><strong>Disease:</strong> {finalReport.disease}</p>
//                 <p><strong>Severity:</strong> {finalReport.severity}</p>

//                 <h2>Symptoms & Care Instructions</h2>
//                 <ReactMarkdown remarkPlugins={[remarkGfm]}>
//                   {finalReport.symptoms_care}
//                 </ReactMarkdown>

//                 <h2 id="page-break">Nearby Hospitals</h2>
//                 <div className="hospital-list">
//                   {finalReport.hospitals && finalReport.hospitals.map((hospital, index) => (
//                     <div key={index} className="hospital-card" onClick={() => window.open(hospital.maps_url, "_blank")}>
//                       <h3>{index + 1}. {hospital.name}</h3>
//                       <p>{hospital.location}</p>
//                       <img
//                         src="https://cdn.mos.cms.futurecdn.net/6MTaNZBnesPxmrTfRCEbQN-1152-80.png"
//                         alt={`Location of ${hospital.name}`}
//                         className="hospital-map"
//                       />
//                     </div>
//                   ))}
//                 </div>
//                 {isOutputReady && (
//                   <button onClick={handleDownloadPDF} className="download-btn">
//                     Download as PDF
//                   </button>
//                 )}
//               </div>
//             )}
//           </>
//         ) : (
//           <h2 className="offline-message">Server Offline. Please try after some time.</h2>
//         )}
//     </div>
//   );
//   // <Footer/>

// }

// export default Upload;



import React, { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import axios from "axios";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import "./Upload.css";

function Upload() {

  const BASE_URL = "http://127.0.0.1:8080";

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [location, setLocation] = useState("");
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [awaitingSymptoms, setAwaitingSymptoms] = useState(false);
  const [finalReport, setFinalReport] = useState(null);
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const outputRef = useRef(null);

  // Check backend once
  useEffect(() => {
    axios.get(`${BASE_URL}/api/status`)
      .then(() => setBackendStatus("Server Online ✅"))
      .catch(() => setBackendStatus("Server Offline ❌"));
  }, []);

  // File select
  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
  };

  // Upload image
  const handleUpload = async () => {
    if (!file || !location.trim()) {
      alert("Upload image and enter location");
      return;
    }

    setIsUploading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(`${BASE_URL}/api/upload`, formData);
      setQuestions(response.data.questions);
      setAwaitingSymptoms(true);
    } catch (err) {
      alert("Upload failed");
    }
    setIsUploading(false);
  };

  // Answer select
  const handleAnswerChange = (symptom, value) => {
    setAnswers({ ...answers, [symptom]: value });
  };

  // Submit symptoms
  const handleSubmitSymptoms = async () => {
    setIsSubmitting(true);

    const response = await axios.post(`${BASE_URL}/api/confirm_symptoms`, {
      answers: answers
    });

    fetchFullDiseaseInfo(response.data.disease, response.data.severity);
  };

  // Get final disease info
  const fetchFullDiseaseInfo = async (disease, severity) => {
    const response = await axios.post(`${BASE_URL}/api/get_disease_info`, {
      disease,
      severity,
      location
    });

    setFinalReport(response.data);
    setIsSubmitting(false);
  };

  // PDF
  const handleDownloadPDF = () => {
    html2canvas(outputRef.current).then(canvas => {
      const img = canvas.toDataURL("image/png");
      const pdf = new jsPDF();
      pdf.addImage(img, "PNG", 0, 0);
      pdf.save("Skin_Report.pdf");
    });
  };

  return (
    <div ref={outputRef} className="upload-container">

      <h3>{backendStatus}</h3>

      {!preview &&
        <input type="file" onChange={handleFileChange} />
      }

      {preview && <img src={preview} alt="preview" width="200" />}

      <input
        type="text"
        placeholder="Enter Location"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
      />

      {!awaitingSymptoms &&
        <button onClick={handleUpload}>
          {isUploading ? "Uploading..." : "Submit"}
        </button>
      }

      {awaitingSymptoms &&
        <div>
          <h3>Answer Symptoms</h3>
          {Object.entries(questions).map(([symptom, question]) => (
            <div key={symptom}>
              <p>{question}</p>
              <button
  className={`yes-btn ${answers[symptom] === "1" ? "selected" : ""}`}
  onClick={() => handleAnswerChange(symptom, "1")}
>
  Yes
</button>

<button
  className={`no-btn ${answers[symptom] === "0" ? "selected" : ""}`}
  onClick={() => handleAnswerChange(symptom, "0")}
>
  No
</button>

            </div>
          ))}

          <button onClick={handleSubmitSymptoms}>
            {isSubmitting ? "Processing..." : "Submit Responses"}
          </button>
        </div>
      }

      {finalReport &&
        <div>
          <h2>Diagnosed Disease</h2>
          <p><b>Disease:</b> {finalReport.disease}</p>
          <p><b>Severity:</b> {finalReport.severity}</p>

          <h3>Symptoms & Care</h3>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {finalReport.symptoms_care}
          </ReactMarkdown>

          <h3>Nearby Hospitals</h3>
          {finalReport.hospitals.map((h, i) => (
            <p key={i}>{h.name} - {h.location}</p>
          ))}

          <button onClick={handleDownloadPDF}>Download PDF</button>
        </div>
      }
    </div>
  );
}

export default Upload;
