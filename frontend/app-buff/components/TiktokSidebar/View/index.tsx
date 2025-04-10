"use client";
import { useState } from "react";

const View = () => {
  const [isCommentEnabled, setIsCommentEnabled] = useState(false); // Trạng thái checkbox "Tạo Bình Luận"

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
                      <input id="checkbox-tim" type="checkbox" value=""  />
                      <label htmlFor="default-checkbox" className="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">Tăng Lượt Tym</label>
              </div>

          <div className="flex items-center mb-4">
            <input
              id="checkbox-comment"
              type="checkbox"
              value=""
              onChange={(e) => setIsCommentEnabled(e.target.checked)} // Cập nhật trạng thái checkbox
            />
            
            <label
              htmlFor="checkbox-comment"
              className="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >
              Tạo Bình Luận
            </label>
          </div>

          <label
            htmlFor="message"
            className={`block mb-2 text-sm font-medium ${
              isCommentEnabled ? "text-gray-900" : "text-gray-400"
            }`}
          >
            Nhập Bình Luận Mà Bạn Muốn
          </label>
          <textarea
            id="message"
            rows={4}
            disabled={!isCommentEnabled} // Vô hiệu hóa textarea nếu checkbox chưa được chọn
            className={`block p-2.5 w-full text-sm ${
              isCommentEnabled
                ? "text-gray-900 bg-gray-50 border-gray-300"
                : "text-gray-400 bg-gray-200 border-gray-200"
            } rounded-lg border focus:ring-blue-500 focus:border-blue-500`}
            placeholder="Write your thoughts here..."
          ></textarea>

          <div className="text-right">
            <button className="bg-blue-500 text-white px-4 py-2 rounded">
              ORDER NGAY
            </button>
          </div>
        </form>
      </main>
    </>
  );
};

export default View;