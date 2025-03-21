import { useContext, useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { DataContext } from "../../context/DataContext"
import AnalysisBox from "../../components/AnalysisBox/AnalysisBox"
import Highlight from "../Highlight/Highlight"
import AssistantBox from "../../components/AssistantBox/AssistantBox"
import './documentPage.less'
import Documents from '../YourDocuments/Documents'
import Wave from '../../img/wave.svg'
import { LuFileText } from "react-icons/lu"

const DocumentPage = () => {
    // Gets global data from the context
    const { crud, access, navigate } = useContext(DataContext)



    // Gets id from the url
    const { id } = useParams()



    // Stores the document
    const [document, setDocument] = useState({})



    // Stores the analysis
    const [analysis, setAnalysis] = useState([])

    //Stores the url
    const [pdfUrl, setPdfUrl] = useState(null)

    //Stores the highlites
    const [keywords, setKeywords] = useState(null)

    //Store review response
    const [review, setReview] = useState(null)



    // Holds the summarized document
    const [summary, setSummary] = useState(null)



    // Gets the document from the backend
    useEffect(() => {
        const handleGetDocument = async () => {
            const response = await crud({
                url: `/api/document/?id=${id}`,
                method: 'get'
            })

            console.log(response)

            if (response.status == 200) {
                const analysisArr = response.data.analysis.map((text) => {
                    return text.trim()
                })
                setDocument(response.data)
                setAnalysis(analysisArr)
                setPdfUrl(response.data.document)
                setKeywords(analysisArr)
            }
        }

        const handleGetReviews = async () => {
            const response = await crud({
                url: `/api/document/review/?document_id=${id}`,
                method: 'get'
            })

            // setReview(response.)
            // console.log(response.data[0])
        }

        if (id) {
            handleGetDocument()
            handleGetReviews()
        }
    }, [id])



    // Gets the summarization
    const handleSummarize = async () => {
        const response = await crud({
            url: `/api/document/summary/?document_id=${id}`,
            method: 'get'
        })

        console.log(response)

        if(response.status == 200) setSummary(response.data.summary)
    }

    // Get review
    const handleReview = async () => {
        const response = await crud({
            url: `/api/document/review/?document_id=${id}`,
            method: 'get'
        })

        // setReview(response.)
        // console.log(response)
    }


    return (
        <section className="section-doc">
            <img src={Wave} className='wave' />
            <div className="result-container">
                <div className="documents-container">
                    <div className="document-box">
                        <div className="title-box">
                            <div className="file-container" onClick={() => navigate(`/document/${document.id}`)}>
                                <div className="file">
                                    <LuFileText className="icon" size={32} color={"#000000"} fill={"#7E4F83"} />
                                    <div className="file-title">
                                        <p className="title">{document.name}</p>
                                    </div>
                                </div>
                
                            </div>
                            <button onClick={handleSummarize} className="btn">Summarize</button>
                        </div>

                        {pdfUrl && <Highlight pdfUrl={pdfUrl} keywords={keywords} />}
                    </div>

                    {
                        summary &&
                        <div className="summary-box">
                            <div className="title-box">
                                <h1>Summary</h1>
                            </div>
                            <p className="summary">{summary}</p>
                        </div>
                    }
                </div>

                <div className="boxes">
                    <AnalysisBox
                        sentences={analysis}
                    />
                    <AssistantBox />
                </div>
            </div>
        </section>
    )
}

export default DocumentPage 