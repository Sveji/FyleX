import Wave from '../../img/wave.svg'
import Upload from '../../img/Group 1.png'
import './main.less'
import '../../globalStyling/components.less'
import { FileUploader } from "react-drag-drop-files"
import { useState, useCallback, useEffect, useContext, useRef } from "react"
import PopUp from '../../components/PopUp/PopUp'
import Login from '../Login/Login'
import Register from '../Register/Register'
import { ImPriceTag } from 'react-icons/im'
import { useDropzone } from 'react-dropzone'
import { MdOutlineCloudUpload } from "react-icons/md";
import { DataContext } from '../../context/DataContext'
import { Link, Outlet } from 'react-router-dom'



const Main = () => {
    // Gets global data from the context
    const { crud, navigate, access } = useContext(DataContext)



    // Stores the file input
    const formData = useRef(new FormData())



    // Sends the file to the backend
    const sendFile = async () => {
        console.log(formData.current.get("document"))
        const response = await crud({
            url: '/api/document/',
            method: 'post',
            body: formData.current
        })

        console.log(response)

        if (response.status == 401) navigate('/login')
        if(response.status == 200) navigate(`/document/${response.data.id}`)

    }



    // Gets the file input
    const onDrop = useCallback((acceptedFiles) => {
        acceptedFiles.forEach((file) => {
            const reader = new FileReader()

            reader.onabort = () => console.log('file reading was aborted')
            reader.onerror = () => console.log('file reading has failed')
            reader.onload = () => {
                // Do whatever you want with the file contents
                const binaryStr = reader.result
                // console.log(binaryStr)
            }

            reader.readAsArrayBuffer(file)
            formData.current.append("document", file)
            formData.current.append("name", file.name)
            formData.current.append("user", access)
            sendFile()
        })

    }, [])

    const { getRootProps, getInputProps } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf', '.docx', '.txt']
        }

    })



    // Sends the request when the user logs in
    useEffect(() => {
        if (access && formData.current.get("document")) sendFile()
    }, [access])



    return (
        <section className="section-main">
            <Outlet />

            <img src={Wave} className='wave shadowed-svg' />

            <div className='text-section'>
                <div className='title-section'>
                    <h1>Scan documents for fraud</h1>
                    <p>Summarize your documents. Identify suspicious parts and consult with an AI model.</p>
                </div>
                {
                    access ?
                        <div className='sub-title'>
                            <p>See your documents and analyses</p>
                            <Link to='/mydocuments' className='login'>here</Link>
                        </div>
                        :
                        <div className='sub-title'>
                            <p>Want to save your analysis?</p>
                            <Link to='/login' className='login'>Login</Link>
                        </div>


                }
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