"use client";


const ViewTiktok =() =>{
    return (
        <>
             <html lang="en">
      <body className="antialiased bg-gray-100">
        <div className="flex h-screen">
          {/* Sidebar */}
          <aside className="w-64 bg-gray-800 text-white flex flex-col">
            <nav className="flex-1">
              <ul className="space-y-2 p-4">
             
                <li className="font-semibold">TIKTOK</li>
                <ul className="pl-4 space-y-1">
                  <li>Tăng mắt live Tiktok</li>
                </ul>
              </ul>
            </nav>
            <footer className="p-4">
            </footer>
          </aside>

          {/* Main Content */}
          <main className="flex-1 p-8 bg-white">
            <h1 className="text-xl font-bold mb-4">Dịch vụ Tiktok</h1>
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
                <label className="block font-semibold mb-1">Chọn Hashtags</label>
                <select className="w-full border border-gray-300 rounded p-2">
                  <option></option>
                </select>
              </div>
              <div>
                <label className="block font-semibold mb-1">Số lượng mắt</label>
                <input
                  type="number"
                  placeholder="100"
                  className="w-full border border-gray-300 rounded p-2"
                />
              </div>
              <div>
                <label className="block font-semibold mb-1">Số phút live</label>
                <input
                  type="number"
                  placeholder="30 phút"
                  className="w-full border border-gray-300 rounded p-2"
                />
              </div>

              <div className="flex items-center mb-4">
                      <input id="default-checkbox" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600" />
                      <label htmlFor="default-checkbox" className="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">Tăng Lượt Tym</label>
                  </div>
                  <div className="flex items-center">
                      <input checked id="default-checkbox" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600" />
                      <label htmlFor="default-checkbox" className="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">Tạo Bình Luận</label>
                  </div>

                  <label htmlFor="message" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Nhập Bình Luận Mà Bạn Muốn</label>
                      <textarea id="message" rows={4} className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Write your thoughts here..."></textarea>
              <div className="text-right">
                <button className="bg-blue-500 text-white px-4 py-2 rounded">
                  ORDER NGAY
                </button>
              </div>
            </form>
           
          </main>
        </div>
      </body>
    </html>
        
        </>
    )



}
export default ViewTiktok;