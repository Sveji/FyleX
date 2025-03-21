import { useContext, useEffect, useState } from "react"
import PopUp from "../../components/PopUp/PopUp"
import { DataContext } from "../../context/DataContext"
import Loading from "../../components/Loading/Loading"
import { useParams } from "react-router-dom"

const Activate = () => {
    // Gets parameters from the url
    const { uidb, token } = useParams()



    // Holds the state for the error
    const [error, setError] = useState(null)



    // Gets global data from the context
    const { access, navigate, crud } = useContext(DataContext)



    // Checks if the user is logged in
    useEffect(() => {
        if(access) navigate('/')
    }, [access])






    // Sends an activation request to the backend
    const handleActivate = async () => {
        const response = await crud({
            url: `/api/user/activate/${uidb}/${token}/`,
            method: 'get'
        })

        if(response.status == 400) {
            setError(response.response.data.error)
        }
        if(response.status == 200) {
            navigate('/login')
        }
    }

    useEffect(() => {
        if(uidb && token) handleActivate()
    }, [uidb, token])



    // Holds the state for the popup
    const [shown, setShown] = useState(true)

    const handleClosePopUp = () => {
        setShown(false)
        setTimeout(() => {
            navigate('/')
        }, 300)
    }



    return (
        <PopUp classes={'account-box'} shown={shown} onClose={handleClosePopUp}>
            <Loading />
            {
                error ?
                <p className="error">{error}</p>
                :
                <h1>Activating account...</h1>
            }
        </PopUp>
    )
}

export default Activate