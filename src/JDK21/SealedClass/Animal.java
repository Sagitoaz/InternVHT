package JDK21.SealedClass;

// chi dog va cat duoc ke thua Animal, bat buoc phai khai bao final, sealed, non-sealed
public sealed class Animal permits Dog, Cat, Bird{
}
