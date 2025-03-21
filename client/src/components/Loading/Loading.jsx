const Loading = () => {
    return (
        <div class="spinner center">
            {
                Array.from({ length: 12 }, _ => null).map((_, i) => (
                    <div class="spinner-blade" key={i}></div>
                ))
            }
        </div>
    )
}

export default Loading