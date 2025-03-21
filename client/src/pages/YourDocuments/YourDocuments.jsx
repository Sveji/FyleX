import './yourdocuments.less'
import Documents from './Documents'
import Wave from '../../img/Wave.svg'
import { useContext, useEffect, useState } from 'react'
import { FaArrowLeft } from "react-icons/fa6";
import { Link } from 'react-router-dom';
import { DataContext } from '../../context/DataContext'

const YourDocuments = () => {
    // Gets global data from the context
    const { crud, access } = useContext(DataContext)



    // Holds the state for the documents
    const [documents, setDocuments] = useState([])



    // Holds the error state of the page
    const [error, setError] = useState(null)



    // Gets the documents from the backend
    useEffect(() => {
        const handleGetDocuments = async () => {
            const response = await crud({
                url: '/api/document/',
                method: 'get'
            })
            console.log(response)

            if(response.status == 200) {
                setDocuments(response.data)
            }
        }

        if (access) handleGetDocuments()
    }, [access])



    // Deletes a document from a user's profile
    const handleDeleteDocument = async (docId) => {
        const response = await crud({
            url: `/api/document/?id=${docId}`,
            method: 'delete'
        })

        console.log(response)

        if(response.status == 200) {
            const newDocs = documents.filter(doc => doc.id !== docId)
            setDocuments(newDocs)
        }
        if(response.status == 400) {
            setError(response.response.data)
        }
    }



    return (
        <>
            <img src={Wave} className='wave' />
            <section className='secs'>
                <div className='title'>
                    <h1>Your documents</h1>
                    <p>Summarize your documents. Identify suspicious parts and consult with an AI model.</p>
                    {error && <p className="error">{error}</p>}
                </div>

                <div className='documents'>
                    {
                        documents.length > 0 &&
                        documents.map((document, i) => (
                            <Documents deleteFunc={() => handleDeleteDocument(document.id)} document={document} key={i} />
                        ))
                    }
                </div>
                <div><Link to='/'><FaArrowLeft color='#C8B3CA' /></Link></div>
            </section>
        </>
    )
}

export default YourDocuments


