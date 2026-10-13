from PIL import Image, ImageDraw
def icon(n, path):
    S = 1024
    im = Image.new('RGB', (S, S), '#3d7fd6')
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((250,150,774,874), 60, fill='#2f67b3', outline='#1f4a85', width=22)
    for y in (215, 265, 315):
        d.rounded_rectangle((350, y, 674, y+22), 11, fill='#1f4a85')
    d.rounded_rectangle((320,420,704,800), 40, fill='#ff7043', outline='#16181d', width=14)
    d.arc((380,280,644,560), 180, 360, fill='#c9ced8', width=34)
    d.ellipse((472,560,552,640), fill='#16181d')
    d.rectangle((503,610,521,720), fill='#16181d')
    im.resize((n, n), Image.LANCZOS).save(path)
icon(512, 'icon-512.png')
icon(192, 'icon-192.png')
icon(180, 'apple-touch-icon.png')
