import { useContext, useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { DataContext } from "../../context/DataContext"
import AnalysisBox from "../../components/AnalysisBox/AnalysisBox"
import Highlight from "../Highlight/Highlight"
import AssistantBox from "../../components/AssistantBox/AssistantBox"
import './documentPage.less'
import Documents from '../YourDocuments/Documents'
import wave from '../../img/wave.svg'
import { LuFileText } from "react-icons/lu"

const DocumentPage = () => {
    // Gets global data from the context
    const { crud, access, navigate } = useContext(DataContext)



    // Checks if user is not logged in
    useEffect(() => {
        if(!access) navigate('/login')
    }, [access])



    // Gets id from the url
    const { id } = useParams()



    // Stores the document
    const [document, setDocument] = useState({})


    //Stores the url
    const [pdfUrl, setPdfUrl] = useState(null)

    //Stores the highlites
    const [keywords, setKeywords] = useState([])

    //Store review response
    const [reviews, setReviews] = useState(null)



    // Holds the summarized document
    const [summary, setSummary] = useState(null)



    // Holds the error state
    const [error, setError] = useState(null)



    // Gets the document from the backend
    useEffect(() => {
        const handleGetDocument = async () => {
            const response = await crud({
                url: `/api/document/?id=${id}`,
                method: 'get'
            })

            console.log(response)

            if (response.status == 200) {
                const reviewsArr = JSON.parse(`[${response.data.review}]`)
                setReviews(reviewsArr)
                setKeywords(reviewsArr.map(review => review['suspicious text'].trim()))
                setDocument(response.data)
                setPdfUrl(response.data.document)
            }

            if(response.status == 400) setError(response.response.data)
        }

        if (id) handleGetDocument()
    }, [id])



    // Gets the summarization
    const handleSummarize = async () => {
        const response = await crud({
            url: `/api/document/summary/?document_id=${id}`,
            method: 'get'
        })

        console.log(response)

        if(response.status == 200) setSummary(response.data.summary)
        if(response.status == 400) setError(response.response.data)
        if(response.status == 500 || response.status == 502) setError(response.response.data.error)
    }


    return (
        <section className="section-doc">
            <img src={wave} className='wave' />
            {
                error ? 
                <p className="error">{error}</p>
                :
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
                            true &&
                            <div className="summary-box">
                                <div className="title-box">
                                    <h1>Summary</h1>
                                </div>
                                {/* <p className="summary">{summary}</p> */}
                                <p className="summary">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Tempora fugit minima dolorum exercitationem officia optio maiores magni quas fugiat excepturi? Beatae dolore et enim aliquam debitis cumque corporis ab quis magnam nemo, facere nulla odio. Dolorum dignissimos explicabo velit harum debitis accusantium iste nam quos, repellat ullam ea neque animi ex amet possimus iusto recusandae aperiam, corporis sit. Sit reprehenderit modi deserunt harum numquam quos iste, tempora cupiditate, voluptatibus earum, exercitationem repellat sequi autem ab voluptas molestias natus a reiciendis.</p>
                            </div>
                        }
                    </div>

                    <div className="boxes">
                        <AnalysisBox
                            sentences={reviews}
                        />
                        <AssistantBox />
                    </div>
                </div>
            }
        </section>
    )
}

export default DocumentPage 