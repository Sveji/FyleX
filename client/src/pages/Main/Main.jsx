import Wave from '../../img/wave.svg'
import Upload from '../../img/Group 1.png'
import './main.less'
import '../../globalStyling/components.less'
import { FileUploader } from "react-drag-drop-files"
import { useState, useCallback } from "react"
// import { ImPriceTag } from 'react-icons/im'
import { useDropzone } from 'react-dropzone'
import { MdOutlineCloudUpload } from "react-icons/md";


const Main = () => {

    const [file, setFile] = useState()


    console.log(file)

    // const clearHandler = () => {
    //     setFile(null)

    // }

    const onDrop = useCallback((acceptedFiles) => {
        acceptedFiles.forEach((file) => {
            const reader = new FileReader()

            reader.onabort = () => console.log('file reading was aborted')
            reader.onerror = () => console.log('file reading has failed')
            reader.onload = () => {
                // Do whatever you want with the file contents
                const binaryStr = reader.result
                console.log(binaryStr)
            }
            reader.readAsArrayBuffer(file)
        })

    }, [])

    const { getRootProps, getInputProps } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf', '.docx', '.txt']
        }

    })

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
                    <div className='uploading' {...getRootProps()}>
                        <input {...getInputProps()} />
                        <div className='inside'>
                            <img src={Upload} alt="" />
                            <div className='text'>
                                <div className='container-text'>
                                    <p>Drag and drop</p>
                                    <p className='purple'>your files here</p>
                                </div>
                                <p> or</p>

                                <div className='upload-icon-container'>
                                    <MdOutlineCloudUpload size={32} />
                                    <p>Upload document</p>
                                </div>

                            </div>
                        </div>

                    </div>
                    {/* <FileUploader
                        dropMessageStyle={{ backgroundColor: 'red' }}
                        // style={{
                        //     border: "2px dashed #916895",
                        // }}
                        classes="drop_zone"
                        multiple={false}
                        name="file"
                        type={["pdf", "txt", "docx"]}
                        handleChange={(file) => setFile(file)}
                    /> */}
                </div>
                {/* <div className='uploaded'>
                    <p>{file ? `File name: ${file.name}` : 'No file uploaded yet!'}</p>
                </div>
                <div className='btn'>
                    <button cnClick={clearHandler} >Cancel</button>
                </div> */}
            </div>

        </section>
    )
}

export default Main