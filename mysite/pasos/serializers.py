class PasosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasos
        fields = '__all__'     
        
    def create(self, validated_data):
        return Pasos.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.pasos_id = validated_data.get('pasos id', instance.pasos_id)
        instance.gestion_id = validated_data.get('gestion id', instance.gestion_id)
        instance.nombre_paso= validated_data.get('nombre paso', instance.nombre_paso)
        instance.orden= validated_data.get('orden', instance.orden)
        instance.save()
        return instance