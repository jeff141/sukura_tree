# 3D 樱花桌面特效

> 🌸 一个用 Python 编写的全屏透明樱花飘落特效，花瓣在树冠层间穿梭，营造 3D 景深感（Windows）。

**作者：一坨肉**  
**邮箱：1561074588@qq.com**  
**开源协议：MIT（使用时请保留作者署名）**

---

### 安装依赖
```
pip install -r requirements.txt
```

### 打包成 exe
```
pyinstaller --noconsole --onefile --windowed --add-data "resources;resources" --icon="icon.ico" tree_v3.py
```

## 目录结构

```
tree/
├── tree_v3.py
├── requirements.txt
├── README.md
└── resources/
    ├── petal.png      # 花瓣
    ├── trunk.png      # 树干
    ├── crown1.png     # 树冠（底层）
    ├── crown2.png     # 树冠（顶层，花瓣从其后穿过）
    └── crown3.png     # 树冠（底层）
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

© 2025 一坨肉. All rights reserved.
