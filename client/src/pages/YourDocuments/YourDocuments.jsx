import './yourdocuments.less'
import Documents from './Documents'
import Wave from '../../img/Wave.svg'

const YourDocuments = () => {

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


