import './yourdocuments.less'
import Documents from './Documents'
import Wave from '../../img/Wave.svg'
import { useContext, useEffect } from 'react'
import { DataContext } from '../../context/DataContext'

const YourDocuments = () => {
    // Gets global data from the context
    const { crud, access } = useContext(DataContext)



    // Gets the documents from the backend
    useEffect(() => {
        const handleGetDocuments = async () => {
            const response = await crud({
                url: '/api/document/',
                method: 'get'
            })
        }

        if(access) handleGetDocuments()
    }, [access])



    return (
        <>
            <img src={Wave} className='wave' />
            <section className='secs'>
                <div className='title'>
                    <h1>Your documents</h1>
                    <p>Summarize your documents. Identify suspicious parts and consult with an AI model.</p>

                </div>

                <div className='documents'>

                    <Documents />
                    <Documents />
                    <Documents />
                </div>
            </section>
        </>
    )
}

export default YourDocuments


