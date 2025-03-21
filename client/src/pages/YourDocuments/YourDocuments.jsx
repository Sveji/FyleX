import './yourdocuments.less'
import Documents from './Documents'
import Wave from '../../img/Wave.svg'
import { FaArrowLeft } from "react-icons/fa6";
import { Link } from 'react-router-dom';

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
                <div><Link to='/'><FaArrowLeft color='#C8B3CA' /></Link></div>
            </section>
        </>
    )
}

export default YourDocuments


