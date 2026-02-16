DAY=day$(date +"%Y%m%d")
echo $DAY >>./christmass/Newyear.txt
git add .
git commit -m $DAY
git push origin Christmass2025
unset DAY
