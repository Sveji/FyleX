import Wave from '../../img/wave.svg'
import './main.less'
import { FileUploader } from "react-drag-drop-files"
import { useState, useCallback } from "react"

const Main = () => {

    const [file, setFile] = useState()
    // const []

    console.log(file)

    const clearHandler = () => {
        setFile(null)

    }

    return (
        <section className="section-main">
            <img src={Wave} className='wave' />

            <div className='text-section'>
                <div className='title-section'>
                    <h1>Scan documents for fraud</h1>
                    <p>Summarize your documents. Identify suspicious parts and consult with an AI model.</p>
                </div>
                <div className='sub-title'>
                    <p>Want to save your analysis?</p>
                    <p className='login'>Login</p>
                </div>
            </div>

            <div className='scan-section'>
                <div className='content'>
                    <FileUploader
                        multiple={false}
                        name="file"
                        type={["pdf", "txt", "docx"]}
                        handleChange={(file) => setFile(file)}
                    />
                </div>
                <div className='uploaded'>
                    {file ? `File name: ${file.name}` : 'No file uploaded yet!'}
                </div>
                <div className='btn'>
                    <button cnClick={clearHandler} >Cancel</button>
                </div>
            </div>

        </section>
    )
}

export default Main