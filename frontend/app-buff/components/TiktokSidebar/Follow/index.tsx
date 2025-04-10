"use client";


const Follow =() =>{
    return (
        <>
          {/* Main Content */}
          <main className="flex-1 p-8 bg-white">
            
            <form className="space-y-4">
              <div>
                <label className="block font-semibold mb-1">Link Tiktok</label>
                <input
                  type="text"
                  
                  placeholder="https://tiktok.com/@username/live"
                  className="w-full border border-gray-300 rounded p-2"
                />
              </div>
              <div>
                <label className="block font-semibold mb-1">Số lượng follow</label>
                <input
                  type="number"
                  placeholder="100"
                  className="w-full border border-gray-300 rounded p-2"
                />
              </div>
              <div className="text-right">
                <button className="bg-blue-500 text-white px-4 py-2 rounded">
                  ORDER NGAY
                </button>
              </div>
            </form>
           
          </main>
      
        
        </>
    )
}
export default Follow;